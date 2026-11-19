"""Copy the pack's mods, config, defaultconfigs and kubejs folders (plus mmc-pack.json) from the
Prism instance into ../pack, using the same filters as make_mrpack.py: no .bak files, no
config files over 2 MB, and no resourceful-config-web.json (it holds a locally generated
password). Deletes ../pack first so removed files disappear too."""
import os, shutil

ROOT = os.path.join(os.environ["APPDATA"], "PrismLauncher", "instances", "MP 1.21.1")
INST = os.path.join(ROOT, "minecraft")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pack")

shutil.rmtree(OUT, ignore_errors=True)
n = 0
for d in ("mods", "config", "defaultconfigs", "kubejs"):
    src = os.path.join(INST, d)
    for root, _, fs in os.walk(src):
        for f in fs:
            p = os.path.join(root, f)
            if ".bak" in f or f == "resourceful-config-web.json" or (d == "config" and os.path.getsize(p) > 2 * 1048576):
                continue
            dst = os.path.join(OUT, d, os.path.relpath(p, src))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(p, dst)
            n += 1
os.makedirs(OUT, exist_ok=True)
shutil.copy2(os.path.join(ROOT, "mmc-pack.json"), os.path.join(OUT, "mmc-pack.json"))
print("copied", n + 1, "files to", os.path.normpath(OUT))
