// Atomic Disassembler now needs materials from Create, Evolved Mekanism, Oritech
// and Modern Industrialization on top of Mekanism's Atomic Alloy and Refined Obsidian.
ServerEvents.recipes(event => {
  event.remove({ id: 'mekanism:atomic_disassembler' })

  event.shaped('mekanism:atomic_disassembler', [
    'SPS',
    'D#D',
    'MIM'
  ], {
    S: 'evolvedmekanism:alloy_subatomic',
    P: 'create:precision_mechanism',
    D: 'oritech:duratium_ingot',
    '#': 'mekanism:alloy_atomic',
    M: 'modern_industrialization:iridium_plate',
    I: '#c:ingots/refined_obsidian'
  }).id('kubejs:atomic_disassembler_hard')
})
