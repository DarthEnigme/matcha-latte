import json,os,glob,hashlib,zipfile,urllib.request,sys
API="https://api.modrinth.com/v2"; H={"User-Agent":"mp-modpack-builder/1.0","Content-Type":"application/json"}
INST=os.path.join(os.environ["APPDATA"],"PrismLauncher","instances","MP 1.21.1","minecraft")
OUT=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"Matcha-Latte-1.21.1.mrpack")
def post(u,d): return json.load(urllib.request.urlopen(urllib.request.Request(API+u,data=json.dumps(d).encode(),headers=H),timeout=60))
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(API+u,headers=H),timeout=60))
jars=sorted(glob.glob(INST+"/mods/*.jar")); info={}
for j in jars:
    b=open(j,"rb").read(); info[j]=(hashlib.sha1(b).hexdigest(),hashlib.sha512(b).hexdigest(),len(b))
found=post("/version_files",{"hashes":[v[0] for v in info.values()],"algorithm":"sha1"})
pids=sorted({v["project_id"] for v in found.values()})
sides={}
for i in range(0,len(pids),50):
    q=json.dumps(pids[i:i+50]); 
    for p in get("/projects?ids="+urllib.parse.quote(q) if False else "/projects?ids="+__import__("urllib.parse").parse.quote(q)): sides[p["id"]]=(p["client_side"],p["server_side"])
files=[];over=[]
for j in jars:
    sha1,sha512,size=info[j]; v=found.get(sha1)
    if v:
        f=next(x for x in v["files"] if x["hashes"]["sha1"]==sha1)
        c,s=sides.get(v["project_id"],("required","required"))
        files.append({"path":"mods/"+os.path.basename(j),"hashes":{"sha1":sha1,"sha512":sha512},"env":{"client":c if c!="unknown" else "required","server":s if s!="unknown" else "required"},"downloads":[f["url"]],"fileSize":size})
    else: over.append(j)
idx={"formatVersion":1,"game":"minecraft","versionId":"1.0.1","name":"Matcha Latte","summary":"Create-focused NeoForge 1.21.1 pack: Create, Mekanism, AE2, Oritech, Modern Industrialization, dimensions and decor.","files":files,"dependencies":{"minecraft":"1.21.1","neoforge":"21.1.266"}}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED) as z:
    z.writestr("modrinth.index.json",json.dumps(idx,indent=2))
    for j in over: z.write(j,"overrides/mods/"+os.path.basename(j))
    cfg=os.path.join(INST,"config"); n=0
    for root,_,fs in os.walk(cfg):
        for f in fs:
            p=os.path.join(root,f)
            if os.path.getsize(p)>2*1048576 or ".bak" in f or f=="resourceful-config-web.json": continue
            z.write(p,"overrides/config/"+os.path.relpath(p,cfg).replace("\\","/")); n+=1
    for d in ("defaultconfigs","kubejs"):
        dd=os.path.join(INST,d)
        for root,_,fs in os.walk(dd):
            for f in fs:
                p=os.path.join(root,f); z.write(p,"overrides/"+d+"/"+os.path.relpath(p,dd).replace("\\","/"))
print("on Modrinth:",len(files),"| bundled:",len(over),"| configs:",n)
print("bundled jars:",[os.path.basename(j) for j in over])
print("size MB:",round(os.path.getsize(OUT)/1048576,1))
