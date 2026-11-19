import json,os,zipfile,tomllib
M=os.path.join(os.environ["APPDATA"],"PrismLauncher","instances","MP 1.21.1","minecraft","mods")
old={r[3]:r for r in json.load(open("mods.json"))}
rows=[];bad=[]
for fn in sorted(os.listdir(M)):
    if not fn.endswith(".jar"): continue
    if fn in old: rows.append(old[fn]); continue
    try:
        with zipfile.ZipFile(os.path.join(M,fn)) as z:
            d=tomllib.loads(z.read("META-INF/neoforge.mods.toml").decode("utf-8"))
        m=d["mods"][0]
        rows.append([m["modId"],m.get("displayName",m["modId"]),str(m.get("version","?")),fn])
    except Exception as e: bad.append((fn,str(e)))
json.dump(rows,open("mods.json","w"),indent=0)
print(len(rows),"bad:",bad)
print([r for r in rows if r[3] not in old])
