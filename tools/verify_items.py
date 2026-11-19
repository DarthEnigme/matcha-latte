import json,difflib,sys
sys.path.insert(0,".")
from quest_data import CATS
import os; d=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"items.json"))); ns={}
for j,v in d.items():
    for k,x in v.items(): ns.setdefault(k,set()).update(x)
ns.setdefault("minecraft",set())
bad=0
for f,t,icon,mods in CATS:
    for name,item,desc in [(None,icon,None)]+[(m[0],m[1],m[2]) for m in mods]:
        if not item or item.startswith("minecraft:"): continue
        n,i=item.split(":")
        if i in ns.get(n,()): continue
        bad+=1
        c=difflib.get_close_matches(i,sorted(ns.get(n,[])),5,0.4)
        sub=[x for x in sorted(ns.get(n,[])) if not x.endswith(("_trim","_spawn_egg")) ][:12] if not c else []
        print("MISSING",name or "ICON:"+t,item,"->",c or ("(ns has %d) "%len(ns.get(n,[]))+" ".join(sub)))
print(bad,"missing")
