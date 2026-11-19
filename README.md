# Matcha Latte

A Create-focused tech and exploration modpack for **Minecraft 1.21.1** on **NeoForge 21.1.266**.

Matcha Latte is built around Create's machines and contraptions, with Mekanism, Applied Energistics 2, Oritech and Modern Industrialization to grow into. Around the tech sit new dimensions, a rebuilt End, harder dungeons, loot to hunt, a lot of food, and enough decoration mods to make your base look good. You can play it as a factory pack, an adventure pack, or both.

> **Status: working draft.** The pack has been tested by one person on one machine in short sessions. It starts and runs without crashes, but much of it has not been played through yet. Bug reports are welcome.

## At a glance

| | |
|---|---|
| Minecraft | 1.21.1 |
| Loader | NeoForge 21.1.266 |
| Mods | 157 mods + 45 libraries (202 jars) |
| Launcher | Prism Launcher (`.mrpack` import) |
| Java | 21 |
| Memory | 8 GB for the game, 12 to 16 GB of RAM in the machine |

## Install

1. Download `Matcha-Latte-1.21.1.mrpack` from the [latest release](../../releases/latest).
2. In [Prism Launcher](https://prismlauncher.org): **Add Instance → Import**, and pick the file. Prism downloads 190 mods from Modrinth. The 12 mods that are only on CurseForge come inside the file.
3. Set memory and Java arguments as described in [`java-settings.md`](java-settings.md): 8192 MB minimum and maximum, plus the G1GC arguments. The `.mrpack` cannot carry these.
4. Optional, in game: render distance 12, simulation distance 8, entity distance 75%. The pack was tuned with these.

The first start takes about a minute to reach the main menu.

## Starting a world

- **Choose the BetterX world type** (More tab of the world creation screen). Without it you get the vanilla End instead of BetterEnd's.
- The first trip into a new End can freeze the game for 20 to 60 seconds while it generates. Wait, it recovers.

## What's inside

**Create and addons.** The heart of the pack. Create plus Crafts & Additions, New Age, Connected, Enchantment Industry, Copycats+, Deco, Encased, Ore Excavation, Ultimate Factory, Ender Transmission, Nuclear, Power Grid, The Factory Must Grow, Applied Kinetics, Railways Navigator, Create Jetpack and more.

**Tech.** Mekanism (with Generators, Tools, Additions and Evolved Mekanism), Oritech, Modern Industrialization, Powah, Flux Networks, Pipez and Just Dire Things. ComputerCraft (CC: Tweaked, Advanced Peripherals) with a bridge to Create.

**Storage and logistics.** Applied Energistics 2 with Expanded AE, Advanced AE, Applied Flux, MEGA Cells, wireless terminals and others, plus backpacks and storage mods.

**Loot, gear and RPG.** The Apotheosis suite, Artifacts, Relics, More Relics, Enigmatic Legacy+, Silent Gear, Advanced Netherite, Lootr (every player gets their own chest loot), Gravestone, Spice of Life: Carrot Edition (eat a varied diet to gain hearts) and Colorful Hearts.

**Dimensions and exploration.** Twilight Forest, The Aether, Undergarden, Deeper and Darker, Eternal Starlight and a rebuilt End with BetterEnd. Cataclysm bosses, When Dungeons Arise, YUNG's structure overhauls, new towns, and Terralith and Tectonic terrain. Waystones for travel.

**Food and farming.** Farmer's Delight and its addons, Croptopia, Brewin' And Chewin', Cooking for Blockheads and Productive Bees.

**Decoration.** Chipped, Macaw's mods, Supplementaries, Handcrafted, Another Furniture, Immersive Furniture, Framed Blocks, Domum Ornamentum and others.

**Quality of life.** JEI, Jade, JourneyMap, AppleSkin, Inventory Essentials, Mouse Tweaks, Construction Wands, FTB Chunks (claim and force-load chunks) and FTB Quests.

**Performance.** Sodium, Iris (bring your own shader pack), Lithium, FerriteCore, ModernFix, ImmediatelyFast, Entity Culling, Noisium, ScalableLux and C2ME.

The full list with versions is in [`tools/mods.json`](tools/mods.json).

## How this pack plays differently

Some changes are made on purpose, to keep progression meaningful:

- **No infinite food.** Everlasting Beef, Eternal Steak and the Infinite Ham are gone from loot, and the Eternal Cake cannot be crafted. The Carrot Edition food-variety system is meant to matter.
- **Fewer easy jetpacks.** Mekanism, Oritech and Modern Industrialization jetpacks (and the MekaSuit jetpack module) have no recipes. Create Jetpack and other flight options still work.
- **Harder structure finders.** Explorer's Compass and Nature's Compass need a Recovery Compass plus materials from Create, the Twilight Forest and the Aether, so you earn them mid-game.
- **A late-game Atomic Disassembler.** Its recipe now needs materials from Mekanism, Evolved Mekanism, Create, Oritech and Modern Industrialization.
- **More accessory slots.** 6 ring slots, and 4 each for necklace, charm, belt, back, hands, bracelet and curio.
- **Loot in BetterEnd's crashed ships.** Their chests use End City treasure loot.
- **Bigger claims.** FTB Chunks allows 999 claimed and 512 force-loaded chunks per player.
- **Quieter Mekanism Additions.** Its baby mob variants do not spawn.
- **Create Nuclear radiation is off.**
- **Unified ores.** Almost Unified merges duplicate ores and ingots (priority: Minecraft, Create, Mekanism, Modern Industrialization, Oritech, TFMG).

## The quest book

Press `O` to open it. It is a guide to the pack rather than a progression line: 9 chapters with one quest per mod, showing what each mod adds, plus 7 chapters of tips. There are no rewards yet.

## Known issues

- The first visit to a new End stalls the game for 20 to 60 seconds.
- The log shows some recipe and loot-table errors and a few missing textures. They are cosmetic and do not affect play.
- BetterEnd's own chests and barrels are not Lootr chests, so their loot is shared.
- C2ME is an alpha mod. If you hit odd world-generation problems, try removing it.
- Mouse Tweaks and Inventory Essentials overlap. Report any double clicks.
- Power Grid and Relics are pinned to older versions for compatibility with other mods.

## What's in this repository

| Path | What it is |
|---|---|
| `Matcha-Latte-1.21.1.mrpack` | The pack (also attached to each release) |
| `java-settings.md` | Memory and Java arguments |
| `pack/` | The instance's `mods` (all 202 jars), `config`, `defaultconfigs` and `kubejs` folders and `mmc-pack.json`. Copy these into a Prism instance's `minecraft` folder as an alternative to the `.mrpack`. The KubeJS scripts with the recipe and loot changes are in `pack/kubejs/server_scripts/` |
| `tools/` | Python scripts that build the `.mrpack`, the mod list and the quest book from a Prism instance (see [`tools/README.md`](tools/README.md)) |

The `.mrpack` is the easier install: it downloads most jars from Modrinth instead of using the copies in `pack/mods`.

All mods belong to their authors. Matcha Latte only collects and configures them.
