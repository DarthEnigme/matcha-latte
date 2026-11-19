import json,os,sys,glob,hashlib,urllib.request,urllib.parse
API="https://api.modrinth.com/v2"; H={"User-Agent":"mp-modpack-builder/1.0","Content-Type":"application/json"}
MODS=os.path.join(os.environ["APPDATA"],"PrismLauncher","instances","MP 1.21.1","minecraft","mods")
def req(u,data=None):
    r=urllib.request.Request(u,data=json.dumps(data).encode() if data else None,headers=H)
    return json.load(urllib.request.urlopen(r,timeout=60))
# installed project ids via hashes
hs={}
for f in glob.glob(MODS+"/*.jar"):
    hs[hashlib.sha512(open(f,"rb").read()).hexdigest()]=f
inst=req(API+"/version_files",{"hashes":list(hs),"algorithm":"sha512"})
have={v["project_id"] for v in inst.values()}
q=urllib.parse.urlencode({"game_versions":'["1.21.1"]',"loaders":'["neoforge"]'})
def newest(p):
    try: vs=req(f"{API}/project/{p}/version?{q}")
    except Exception: return None
    if not vs: return None
    rel=[v for v in vs if v["version_type"]=="release"] or vs
    return sorted(rel,key=lambda v:v["date_published"],reverse=True)[0]
queue=sys.argv[1:]; done={}; miss=[]
while queue:
    s=queue.pop(0)
    v=newest(s)
    if not v: miss.append(s); continue
    if v["project_id"] in have or v["project_id"] in done: continue
    done[v["project_id"]]=(s,v)
    for d in v["dependencies"]:
        if d["dependency_type"]=="required" and d["project_id"] and d["project_id"] not in have and d["project_id"] not in done: queue.append(d["project_id"])
for pid,(s,v) in done.items():
    f=next((x for x in v["files"] if x["primary"]),v["files"][0])
    data=urllib.request.urlopen(urllib.request.Request(f["url"],headers=H),timeout=120).read()
    ok=hashlib.sha512(data).hexdigest()==f["hashes"]["sha512"]
    if ok: open(os.path.join(MODS,f["filename"]),"wb").write(data)
    print(("OK  " if ok else "BAD "),s,f["filename"])
print("missing:",miss)
