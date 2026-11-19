# Writes items.json: for each installed mod jar, the item model names per namespace.
# verify_items.py uses it to check the item IDs in quest_data.py and tips_data.py.
import zipfile,glob,re,json,os,collections
MODS=os.path.join(os.environ["APPDATA"],"PrismLauncher","instances","MP 1.21.1","minecraft","mods")
out={}
for j in sorted(glob.glob(MODS+"/*.jar")):
    z=zipfile.ZipFile(j); ns=collections.defaultdict(set)
    for n in z.namelist():
        m=re.match(r"assets/([^/]+)/models/item/([^/]+)\.json$",n)
        if m: ns[m.group(1)].add(m.group(2))
    out[os.path.basename(j)]={k:sorted(v) for k,v in ns.items() if v}
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"items.json"),"w"))
print(len(out),"jars")
