import json, os, sys, hashlib, urllib.request, urllib.parse, concurrent.futures as cf

API = "https://api.modrinth.com/v2"
UA = {"User-Agent": "mp-modpack-builder/1.0"}
GV, LOADER = "1.21.1", "neoforge"
INST = os.path.join(os.environ["APPDATA"], "PrismLauncher", "instances", "MP 1.21.1")
MODS = os.path.join(INST, "minecraft", "mods")
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# name -> slug (None = search by name)
WANT = """
create|create-interiors|createaddition|create-new-age|create-stuff-additions|create-enchantment-industry|create-jetpack|create-ore-excavation|create-deco|create-connected|create-mechanical-spawner|create-steam-n-rails|create-confectionery|create-dragons-plus|create-cobblestone
mekanism|mekanism-generators|mekanism-tools|mekanism-additions|mekanism-extras|evolved-mekanism
ae2|expanded-ae|merequester|applied-flux|ae2-wireless-terminals|ae2-crafting-tree|ae2-additional-lights|megacells|advanced-ae
flux-networks|oritech|just-dire-things|modern-industrialization|powah|ender-io
apotheosis|apothic-attributes|apothic-enchanting|apothic-spawners|artifacts|relics|more-relics|curios|explorers-compass|natures-compass
terralith|yungs-better-dungeons|yungs-better-mineshafts|yungs-better-strongholds|yungs-better-desert-temples|yungs-better-ocean-monuments|yungs-better-nether-fortresses|yungs-better-end-island|yungs-better-witch-huts|yungs-better-jungle-temples|tectonic|when-dungeons-arise|alexs-mobs|alexs-caves|waystones|biomes-o-plenty|towns-and-towers|structory
chipped|macaws-doors|macaws-windows|macaws-furniture|macaws-roofs|macaws-bridges|macaws-fences-and-walls|macaws-lights-and-lamps|macaws-trapdoors|macaws-paintings|supplementaries|handcrafted|every-compat|framedblocks|amendments|moonlight
croptopia|farmers-delight|oh-the-biomes-weve-gone-farmers-delight|brewin-and-chewin|enders-delight|nethers-delight|fruits-delight|farmers-croptopia|cooking-for-blockheads|farmers-respite|miners-delight|delightful|croptopia-delight
sophisticated-backpacks|sophisticated-storage|jei|jade|journeymap|appleskin|sodium|iris|lithium|ferritecore|modernfix|entityculling|mouse-tweaks|controlling|inventory-profiles-next|architectury-api|cloth-config|bookshelf|balm|geckolib|patchouli|resourceful-lib|resourceful-config|yacl|fusion-connected-textures|jade-addons-neo|emi|konkrete|searchables|fastsuite|ftb-chunks|ftb-teams|ftb-library
""".replace("\n", "|").split("|")
WANT = [w.strip() for w in WANT if w.strip() and w.strip() != "emi"]  # JEI only

def get(url):
    r = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(r, timeout=60) as f:
        return json.load(f)

def versions(slug):
    q = urllib.parse.urlencode({"game_versions": json.dumps([GV]), "loaders": json.dumps([LOADER])})
    try:
        return get(f"{API}/project/{slug}/version?{q}")
    except Exception:
        return None

def search(name):
    facets = json.dumps([["project_type:mod"], [f"versions:{GV}"], [f"categories:{LOADER}"]])
    q = urllib.parse.urlencode({"query": name.replace("-", " "), "facets": facets, "limit": 3})
    try:
        hits = get(f"{API}/search?{q}")["hits"]
        return hits[0]["slug"] if hits else None
    except Exception:
        return None

def pick(vs):
    rel = [v for v in vs if v["version_type"] == "release"] or vs
    rel.sort(key=lambda v: v["date_published"], reverse=True)
    return rel[0]

resolved, missing, queue, seen = {}, [], list(WANT), set()
def resolve(slug):
    vs = versions(slug)
    if not vs:
        alt = search(slug)
        if alt and alt != slug:
            vs = versions(alt); slug = alt
    return slug, (pick(vs) if vs else None)

while queue:
    batch, queue = queue, []
    with cf.ThreadPoolExecutor(8) as ex:
        results = list(ex.map(lambda s: (s, resolve(s)), [b for b in batch if b not in seen]))
    for orig, (slug, v) in results:
        seen.add(orig)
        if not v:
            missing.append(orig); continue
        pid = v["project_id"]
        if pid in resolved: continue
        resolved[pid] = (slug, v)
        for d in v["dependencies"]:
            if d["dependency_type"] == "required" and d["project_id"] and d["project_id"] not in resolved:
                queue.append(d["project_id"])
    # dependency queue entries are project IDs; slug lookup accepts ids too
print(f"resolved {len(resolved)}, missing {len(missing)}")

os.makedirs(MODS, exist_ok=True)
def dl(item):
    slug, v = item
    f = next((x for x in v["files"] if x["primary"]), v["files"][0])
    path = os.path.join(MODS, f["filename"])
    if os.path.exists(path): return slug, f["filename"], "cached"
    data = urllib.request.urlopen(urllib.request.Request(f["url"], headers=UA), timeout=120).read()
    if hashlib.sha512(data).hexdigest() != f["hashes"]["sha512"]:
        return slug, f["filename"], "HASH MISMATCH"
    open(path, "wb").write(data)
    return slug, f["filename"], "ok"

with cf.ThreadPoolExecutor(6) as ex:
    res = list(ex.map(dl, resolved.values()))
bad = [r for r in res if r[2] not in ("ok", "cached")]

# Prism instance
nf = "21.1.266"
json.dump({"components": [
    {"uid": "net.minecraft", "version": GV, "important": True},
    {"uid": "net.neoforged", "version": nf}], "formatVersion": 1},
    open(os.path.join(INST, "mmc-pack.json"), "w"), indent=2)
open(os.path.join(INST, "instance.cfg"), "w").write(
    "[General]\nConfigVersion=1.2\nname=MP 1.21.1\nOverrideMemory=true\nMinMemAllocation=4096\n"
    "MaxMemAllocation=8192\nOverrideJavaArgs=false\niconKey=default\nInstanceType=OneSix\n")

with open(os.path.join(OUT, "modlist.md"), "w", encoding="utf-8") as f:
    f.write("# MP 1.21.1 NeoForge modpack\n\n## Installed\n")
    for slug, fn, st in sorted(res): f.write(f"- {slug}: {fn} ({st})\n")
    f.write("\n## Not found on Modrinth for 1.21.1 NeoForge (manual/CurseForge)\n")
    for m in sorted(missing): f.write(f"- {m}\n")
print("failed downloads:", bad)
print("missing:", sorted(missing))
