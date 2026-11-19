# Java and performance settings for Matcha Latte 1.21.1

These are not stored in the .mrpack. Apply them in Prism: right-click the instance, Edit, Settings, Java.

## Memory
- Minimum memory (Xms): 8192 MB
- Maximum memory (Xmx): 8192 MB
- Same value on purpose, so the heap does not resize mid-game.
- Java 21 (tested with Prism's bundled java-runtime-delta and Temurin 21).
- Needs a machine with at least 12-16 GB of RAM. Close other apps while playing.

## JVM arguments
Tick "Java arguments" and paste (one line):

```
-XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -XX:+UseStringDeduplication
```

`-XX:+AlwaysPreTouch` was deliberately left out (it claims all 8 GB at startup).

## In-pack settings (already inside the .mrpack config, or set in game)
- ModernFix dynamic resources: `config/modernfix-mixins.properties` has `mixin.perf.dynamic_resources=true` (in the .mrpack).
  If you see invisible or purple-black blocks, delete that line.
- Simulation distance 8 (default is 12), entity distance scaling 0.75, render distance 12. These live in `options.txt`, which is NOT in the .mrpack. Set them in game under Video settings.

## Performance mods in the pack
Sodium, Sodium Extra, Iris, Lithium, FerriteCore, ModernFix, Entity Culling, ImmediatelyFast, Dynamic FPS, Noisium, ScalableLux, C2ME (alpha).

## Measured effect on the test machine (6-core CPU, 15 GB RAM)
- Heap in world: about 5.9 GB before the Java flags, about 4.0 GB after.
- Main menu to in-game: about 203 s before tuning, 70-90 s after.
- Worst server lag at join: 20 s behind before, about 2 s after.
These were single runs and varied between launches.
