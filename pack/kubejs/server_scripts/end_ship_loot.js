// BetterEnd's "crashed ship" reuses vanilla's End City ship template but never gives its chests a
// loot table, so they stay empty and Lootr cannot convert them.
// This gives those chests the same loot table as the other End ships (end_city_treasure).
//
// Safe by design: it only runs on the server thread, never loads or generates chunks
// (getChunkNow), runs once every 2 seconds per player, and only touches chests that are
//   - vanilla chests in minecraft:the_end, empty, with no loot table,
//   - in pairs exactly 2 blocks apart (how the ship places them),
//   - in a chunk players have barely spent time in (inhabited time under 1200 ticks).
// Chests you place yourself in a chunk you have been in for a while are never touched.

const EndShipLoot = {
  RL: Java.loadClass('net.minecraft.resources.ResourceLocation'),
  RKey: Java.loadClass('net.minecraft.resources.ResourceKey'),
  Registries: Java.loadClass('net.minecraft.core.registries.Registries'),
  BuiltInRegistries: Java.loadClass('net.minecraft.core.registries.BuiltInRegistries'),
  failed: false,
  // Chunks players have spent more than 60 s (1200 ticks) in are left alone.
  INHABITED_LIMIT: 1200
}
EndShipLoot.TABLE = EndShipLoot.RKey.create(EndShipLoot.Registries.LOOT_TABLE, EndShipLoot.RL.parse('minecraft:chests/end_city_treasure'))

PlayerEvents.tick(event => {
  if (EndShipLoot.failed) return
  var p = event.player
  if (p.tickCount % 40 !== 0) return
  var lvl = p.level
  if (lvl.isClientSide()) return
  if (String(lvl.dimension) !== 'minecraft:the_end') return
  try {
    var px = p.blockPosition().getX() >> 4
    var pz = p.blockPosition().getZ() >> 4
    var src = lvl.getChunkSource()
    for (var dx = -6; dx <= 6; dx++) {
      for (var dz = -6; dz <= 6; dz++) {
        var ch = src.getChunkNow(px + dx, pz + dz)
        if (ch == null) continue
        if (ch.getInhabitedTime() >= EndShipLoot.INHABITED_LIMIT) continue
        var cands = []
        ch.getBlockEntities().values().forEach(be => {
          if (String(EndShipLoot.BuiltInRegistries.BLOCK.getKey(be.getBlockState().getBlock())) !== 'minecraft:chest') return
          if (be.getLootTable() != null) return
          if (!be.isEmpty()) return
          cands.push(be)
        })
        if (cands.length < 2) continue
        cands.forEach(a => {
          var ap = a.getBlockPos()
          var hasPartner = cands.some(b => {
            if (b === a) return false
            var bp = b.getBlockPos()
            if (bp.getY() !== ap.getY()) return false
            var ddx = Math.abs(bp.getX() - ap.getX())
            var ddz = Math.abs(bp.getZ() - ap.getZ())
            return (ddx === 2 && ddz === 0) || (ddz === 2 && ddx === 0)
          })
          if (!hasPartner) return
          if (a.getLootTable() != null) return
          a.setLootTable(EndShipLoot.TABLE, lvl.getRandom().nextLong())
          a.setChanged()
          console.info('[end_ship_loot] gave end_city_treasure to chest at ' + ap.getX() + ' ' + ap.getY() + ' ' + ap.getZ())
        })
      }
    }
  } catch (e) {
    if (!EndShipLoot.failed) {
      EndShipLoot.failed = true
      console.error('[end_ship_loot] disabled after error: ' + e)
    }
  }
})
