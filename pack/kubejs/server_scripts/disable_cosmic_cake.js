// Disables crafting of the Eternal Cake (Enigmatic Legacy+ cosmic cake), a self-restoring food block.
ServerEvents.recipes(event => {
  event.remove({ id: 'enigmaticlegacyplus:cosmic_cake' })
})
