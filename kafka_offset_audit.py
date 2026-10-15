"""Offline, bounded captured-input analysis. Original implementation, MIT."""
import argparse
import json
import re
import sys
from pathlib import Path

class InputError(ValueError):
    pass

def obj(x,required,optional=()):
    if not isinstance(x,dict) or set(x)-set(required)-set(optional) or set(required)-set(x):
        raise InputError("object keys do not match the documented contract")
    return x

def arr(x,limit=512):
    if not isinstance(x,list) or len(x)>limit:raise InputError("expected a bounded array")
    return x

def text(x):
    if not isinstance(x,str) or not 1<=len(x)<=256:raise InputError("expected a nonempty string <=256 characters")
    return x

def integer(x,maximum=9223372036854775807):
    if type(x) is not int or not 0<=x<=maximum:raise InputError("expected bounded nonnegative integer")
    return x

def unique(xs):
    if len(set(xs))!=len(xs):raise InputError("duplicate identity")
    return xs

def pairs(ps):
    d={}
    for k,v in ps:
        if k in d:raise InputError("duplicate JSON key")
        d[k]=v
    return d

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("snapshot",type=Path);a=p.parse_args()
    try:
        with a.snapshot.open("rb") as f:raw=f.read(2*1024*1024+1)
        if len(raw)>2*1024*1024:raise InputError("snapshot exceeds2 MiB")
        d=json.loads(raw.decode("utf-8"),object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(InputError("nonfinite JSON")))
        result=analyze(d);print(json.dumps(result,sort_keys=True,ensure_ascii=True));return 1 if result.get("findings") else 0
    except (InputError,ValueError,TypeError,KeyError,OSError,RecursionError) as e:
        print(json.dumps({"error":str(e)}),file=sys.stderr);return 2

def analyze(d):
    obj(d,["partitions","reset"])
    if d["reset"] not in ("earliest","latest","none"):raise InputError("unknown reset policy")
    keys=[];results=[];findings=[]
    for p in arr(d["partitions"]):
        obj(p,["topic","partition","log_start","log_end","committed"],["requested"])
        key=(text(p["topic"]),integer(p["partition"],2147483647));keys.append(key)
        lo=integer(p["log_start"]);hi=integer(p["log_end"])
        if lo>hi:raise InputError("log start exceeds end")
        c=p["committed"]
        if c is not None:integer(c)
        status="missing_commit" if c is None else "retention_gap" if c<lo else "ahead_of_end" if c>hi else "in_range"
        effective=c if status=="in_range" else lo if d["reset"]=="earliest" else hi if d["reset"]=="latest" else None
        r={"topic":key[0],"partition":key[1],"status":status,"committed_next_offset":c,"captured_start":lo,"captured_end":hi,"hypothetical_start":effective,"offset_distance_to_end":None if effective is None else hi-effective,"reset_required":status!="in_range"}
        if status!="in_range":findings.append({"topic":key[0],"partition":key[1],"kind":status})
        if "requested" in p:
            q=integer(p["requested"])
            if not lo<=q<=hi:raise InputError("requested next offset is outside captured bounds")
            r["requested_next_offset"]=q
            r["movement"]=None if effective is None else {"kind":"skip" if q>effective else "replay" if q<effective else "unchanged","offset_distance":abs(q-effective)}
            if effective is None or q!=effective:findings.append({"topic":key[0],"partition":key[1],"kind":"requested_offset_needs_review"})
        results.append(r)
    unique(keys)
    return {"partitions":sorted(results,key=lambda x:(x["topic"],x["partition"])),"findings":findings,"offset_distances_are_not_record_counts":True,"writes_performed":False}

if __name__ == "__main__":
    raise SystemExit(main())
