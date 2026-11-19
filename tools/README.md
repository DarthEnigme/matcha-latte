# Build scripts for Matcha Latte 1.21.1

Run every script from this folder (`tools`). They read the Prism instance at
`%APPDATA%\PrismLauncher\instances\MP 1.21.1` and write into the parent folder (the repo root).

| Script | What it does |
|---|---|
| `regen_mods.py` | Rescans the instance `mods` folder and updates `mods.json` (name, id, version, file) |
| `make_lists.py` | Writes `../modlist.md` and `../modlist-discord.md` from `mods.json`. The "Fixes and tweaks" text for the Discord list lives in this file |
| `make_mrpack.py` | Builds `../Matcha-Latte-1.21.1.mrpack` (Modrinth downloads by hash, other jars bundled, plus `config`, `defaultconfigs` and `kubejs`). Needs internet |
| `sync_pack.py` | Copies `mods`, `config`, `defaultconfigs`, `kubejs` and `mmc-pack.json` from the instance into `../pack` (same filters as `make_mrpack.py`), so the repo holds the current configs |
| `add_mods.py`, `build_pack.py` | Older scripts used to add mods from Modrinth and to build the first version of the pack |
| `dump_items.py` | Writes `items.json` (item IDs per mod) for the quest scripts |
| `verify_items.py` | Checks every item ID in `quest_data.py` exists in the installed mods |
| `quest_data.py`, `tips_data.py` | The quest book content: one quest per mod, and the tips |
| `build_quests.py` | Writes the quest book into the instance (`config/ftbquests/quests`). It overwrites those files, so edits made in the in-game quest editor are lost |

Typical order after changing mods or configs: `regen_mods.py`, `make_lists.py`, `sync_pack.py`, `make_mrpack.py`, then commit and push.

`make_mrpack.py` and `sync_pack.py` skip `.bak` files, config files over 2 MB and `config/resourceful-config-web.json` (it holds a password generated on this machine).
After editing quests: `dump_items.py` (if mods changed), `verify_items.py`, `build_quests.py`, then restart the game.
