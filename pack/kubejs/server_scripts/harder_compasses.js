// Makes the Explorer's Compass and Nature's Compass late-game items that need
// Create, Twilight Forest and Aether materials plus a Recovery Compass.
// The repair recipes (existing compass + vanilla compass) are left alone.
ServerEvents.recipes(event => {
  event.remove({ id: 'explorerscompass:explorers_compass' })
  event.remove({ id: 'naturescompass:natures_compass' })

  // Explorer's Compass (finds structures)
  event.shaped('explorerscompass:explorerscompass', [
    'KPK',
    'ERE',
    'FGF'
  ], {
    K: 'twilightforest:knightmetal_ingot',
    P: 'create:precision_mechanism',
    E: 'minecraft:ender_eye',
    R: 'minecraft:recovery_compass',
    F: 'twilightforest:fiery_ingot',
    G: 'aether:enchanted_gravitite'
  }).id('kubejs:explorers_compass_hard')

  // Nature's Compass (finds biomes)
  event.shaped('naturescompass:naturescompass', [
    'ZMZ',
    'PRP',
    'ASA'
  ], {
    Z: 'twilightforest:naga_scale',
    M: 'aether:victory_medal',
    P: 'create:precision_mechanism',
    R: 'minecraft:recovery_compass',
    A: 'twilightforest:carminite',
    S: 'twilightforest:fiery_tears'
  }).id('kubejs:natures_compass_hard')
})
