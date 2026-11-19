// Disables crafting of the Mekanism, Oritech and Modern Industrialization jetpacks.
// Create Jetpack, Create Stuff 'N Additions jetpacks and other flight sources are left alone.
ServerEvents.recipes(event => {
  var items = [
    // Mekanism (module_jetpack_unit is the MekaSuit jetpack module)
    'mekanism:jetpack',
    'mekanism:jetpack_armored',
    'mekanism:module_jetpack_unit',
    // Oritech (the boosted elytras are jetpack + elytra combos)
    'oritech:jetpack',
    'oritech:exo_jetpack',
    'oritech:jetpack_elytra',
    'oritech:jetpack_exo_elytra',
    // Modern Industrialization
    'modern_industrialization:diesel_jetpack'
  ]
  items.forEach(function (id) {
    event.remove({ output: id })
  })
})
