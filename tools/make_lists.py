import json,re,collections
import os; S=os.path.dirname(os.path.abspath(__file__))+"/"
rows=json.load(open(S+"mods.json"))
LIBS=set("epherolib creativecore octolib placebo searchables terrablender yungsapi architectury athena balm bookshelf caelus cloth_config cristellib curios dragonlib fusion geckolib guideme igleelib kotlinforforge lionfishapi lithostitched lodestone manascore mechanicals mezz_config moonlight owo glodium ftblibrary patchouli resourcefulconfig resourcefullib sophisticatedcore silentlib supermartijn642corelib titanium yet_another_config_lib_v3 konkrete rhino baguettelib betteradvancedtooltips bclib wover wunderlib".split())
C={}
def put(cat,ids):
    for i in ids.split(): C[i]=cat
put("Create and addons","create createaddition create_new_age create_sa create_connected create_enchantment_industry create_jetpack createoreexcavation create_mechanical_spawner create_confectionery create_dragons_plus createcobblestone createdeco createcasing copycats create_ultimate_factory createendertransmission createnuclear createrailwaysnavigator createaddoncompatibility createappliedkinetics powergrid tfmg interiors cccbridge")
put("Tech and energy","mekanism mekanismadditions mekanismgenerators mekanismtools evolvedmekanism oritech modern_industrialization powah fluxnetworks pipez justdirethings jdttimeaccelerators computercraft advancedperipherals")
put("Applied Energistics 2 and addons","ae2 expandedae advanced_ae appflux merequester megacells ae2wtlib ae2ct")
put("Loot, gear and RPG","apotheosis apothic_attributes apothic_enchanting apothic_spawners artifacts relics morerelics reliquified_twilight_forest enigmaticlegacyplus silentgear advancednetherite bhc cloudboots paraglider colorfulhearts solcarrot explorerscompass naturescompass lootr gravestone gravestonecurioscompat")
put("Dimensions and exploration","twilightforest aether undergarden deeperdarker eternal_starlight betterend cataclysm dungeons_arise dungeons_arise_seven_seas t_and_t mr_tidal_towns waystones terralith tectonic betterdeserttemples betterdungeons betterendisland betterjungletemples bettermineshafts betterfortresses betteroceanmonuments betterstrongholds")
put("Food and farming","farmersdelight croptopia croptopiadelight farmers_croptopia brewinandchewin endersdelight fruitsdelight minersdelight mynethersdelight cookingforblockheads productivebees starcatcher")
put("Storage","sophisticatedbackpacks sophisticatedstorage functionalstorage")
put("Decoration and cosmetics","chipped framedblocks handcrafted another_furniture immersive_furniture mcwbridges mcwdoors mcwlights mcwfences mcwwindows mcwpaintings mcwroofs mcwtrpdoors supplementaries amendments architects_palette decorative_blocks comforts connectiblechains fairylights domum_ornamentum xtonesreworked simplehats cosmeticarmorreworkedforked")
put("QoL and performance","jei jade jadeaddons journeymap appleskin mousetweaks controlling ok_zoomer fastsuite dynamic_fps sodium sodium_extra iris lithium ferritecore modernfix entityculling immediatelyfast noisium scalablelux c2me almostunified ftbchunks ftbteams kubejs constructionwand ftbquests ftbxmodcompat inventoryessentials")
def ver(r):
    v=r[2]
    if "${" in v or v=="?":
        m=re.search(r"(\d+(?:\.\d+)+[^\s]*?)(?:\.jar)$",r[3]); return m.group(1) if m else "-"
    return v
name=lambda r: r[1].replace("-NeoForge","") if r[1] else r[0]
mods=[r for r in rows if r[0] not in LIBS]; libs=[r for r in rows if r[0] in LIBS]
unm=[r for r in mods if r[0] not in C]
by=collections.defaultdict(list)
for r in mods: by[C.get(r[0],"Other")].append(r)
order=["Create and addons","Tech and energy","Applied Energistics 2 and addons","Loot, gear and RPG","Dimensions and exploration","Food and farming","Storage","Decoration and cosmetics","QoL and performance","Other"]
with open(S+"../modlist.md","w",encoding="utf-8") as f:
    f.write(f"# Matcha Latte 1.21.1 NeoForge modpack\n\nMinecraft 1.21.1, NeoForge 21.1.266. {len(rows)} jars: {len(mods)} mods + {len(libs)} libraries. Heap 8 GB.\n\n")
    for c in order:
        if not by[c]: continue
        f.write(f"## {c} ({len(by[c])})\n"); 
        for r in sorted(by[c],key=lambda r:name(r).lower()): f.write(f"- {name(r)} {ver(r)}\n")
        f.write("\n")
    f.write(f"## Libraries ({len(libs)})\n")
    for r in sorted(libs,key=lambda r:name(r).lower()): f.write(f"- {name(r)} {ver(r)}\n")
    f.write("\n## Not on Modrinth for 1.21.1 NeoForge (copied from other instances)\nJust Dire Things, Flux Networks, Croptopia (+EpheroLib), MEGA Cells, FTB Library/Teams/Chunks/Quests/XMod Compat, Domum Ornamentum, Xtones Reworked, Twilight Forest, Spice of Life: Carrot Edition.\n\n## Known issues\n- ~16 recipe errors (mostly Silent Gear netherwood), 25 loot-table errors (Create Casing, Create Connected), a few missing models; all cosmetic.\n- FTB Quests has no quests yet (empty book). KubeJS has no scripts yet.\n- Power Grid pinned to 0.6.0.1 (needs TFMG 1.2.x). Relics pinned to 0.10.7.8 (Reliquified Twilight Forest requires it).\n- C2ME is alpha.\n- BetterEnd only applies in worlds created with the BetterX world type. First entry into a new End takes 20-60 s of server lag. BetterEnd chests and barrels are not Lootr containers.\n- Disabled on purpose: Everlasting Beef and Eternal Steak (Artifacts config), Infinite Ham loot (config/relics/relics/infinity_ham.yaml, needs enabledExtendedConfigs in relics.yaml), Eternal Cake recipe (kubejs/server_scripts/disable_cosmic_cake.js).\n- Mekanism Additions baby mobs are disabled (config/Mekanism/additions.toml, shouldSpawn=false for all six).\n- Create Nuclear radiation is turned off in config (enabled_item_radiation=false): its biome check forced blocking chunk loads in the End.\n")
with open(S+"../modlist-discord.md","w",encoding="utf-8") as f:
    f.write(f"**Matcha Latte 1.21.1 NeoForge modpack** ({len(mods)} mods)\n\n")
    for c in order:
        if not by[c]: continue
        f.write(f"**{c}**\n"+", ".join(name(r) for r in sorted(by[c],key=lambda r:name(r).lower()))+"\n\n")
with open(S+"../modlist-discord.md","a",encoding="utf-8") as f:
    f.write("**Fixes and tweaks in this pack**"+chr(10))
    f.write("- BetterEnd crashed ships: their chests were empty. A KubeJS script (end_ship_loot.js) now gives them the End City ship loot table (end_city_treasure)."+chr(10))
    f.write("- BetterEnd needs the BetterX world type when you create a world. Otherwise the End stays vanilla."+chr(10))
    f.write("- First visit to a new BetterEnd End takes 20-60 s of server lag while it generates."+chr(10))
    f.write("- Create Nuclear radiation is switched off in config (its biome check was making the server wait on chunk loads in the End)."+chr(10))
    f.write("- Disabled (config/script): Everlasting Beef and Eternal Steak (Artifacts), Infinite Ham (Relics, no longer in loot), Eternal Cake recipe (Enigmatic Legacy+). Epoch Apple (More Relics) has no loot source."+chr(10))
    f.write("- Jetpacks from Mekanism (Jetpack, Armored Jetpack, MekaSuit jetpack module), Oritech (Jetpack, Exo Jetpack, Boosted Elytra, Boosted Exo Elytra) and Modern Industrialization (Diesel Jetpack) can no longer be crafted (script disable_jetpacks.js). Create Jetpack and the Create Stuff 'N Additions jetpacks are still craftable."+chr(10))
    f.write("- Explorer's Compass and Nature's Compass have much harder recipes (script harder_compasses.js): each needs a Recovery Compass plus Create, Twilight Forest and Aether materials (for example Precision Mechanisms, Knightmetal, Naga Scales, Enchanted Gravitite, Victory Medal). Repair recipes are unchanged."+chr(10))
    f.write("- Atomic Disassembler has a harder recipe (script atomic_disassembler.js) using Evolved Mekanism Subatomic Alloy, Create Precision Mechanism, Oritech Duratium and Modern Industrialization Iridium Plate."+chr(10))
    f.write("- More Curios slots (datapack): rings 6, and necklace, charm, belt, back, hands, bracelet and curio 4 each."+chr(10))
    f.write("- FTB Chunks limits raised: 999 claimed chunks and 512 force-loaded chunks per team (config)."+chr(10))
    f.write("- FTB Quests book is a reminder of the mods in the pack: one quest per mod in 9 chapters, each asking for one item (or just a click for background mods), plus 7 chapters of tips (Getting Started, Tech, Exploration, Combat and Loot, Building, Food, Storage). Open it with O."+chr(10))
    f.write("- Mekanism Additions baby mobs (Bogged, Creeper, Enderman, Skeleton, Stray, Wither Skeleton) no longer spawn (config)."+chr(10))
    f.write("- Spice of Life: Onion was replaced by Spice of Life: Carrot Edition. YUNG's Better End Island and Stellarity are not included (BetterEnd handles the End)."+chr(10))
print(len(rows),len(mods),len(libs),"unmapped:",[r[0] for r in unm])
import os; print(os.path.getsize(S+"../modlist-discord.md"),"bytes discord")
