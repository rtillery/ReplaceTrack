# ReplaceTrack

Tool to replace audio track with another, matching the original timing, duration, and level.

This tool was created to replace tracks in rhythm games, like Clone Hero, that are corrupted in some way, with a higher quality version. However, to maintain compatibility with the timing of the game portion, in a .mid (.midi) or .chart file, the replacement track needs to match the timing of the original one.

### WIP

This tool is a work in progress. At present, the intended approach is:

1. Detect the start of each track using a silence threshold.
2. Use the starts to do a coarse alighment of the tracks by adjusting the start of the replacement track to match the original. (It is assumed that, because the tracks have different sources, a simple silcence threshold will not be enough for fine alignment, which will be done later).
3. Adjust the start of the replacement track to match the original coarse value. This may involve cropping the intro silence or extending it with additional silence.
4. Detect the end of each track using a silence threshold.
5. Use the ends to do a coarse alignment of the tracks by cropping or prepending the replacement track to match the original.
6. Calculate the audio length (end - start) of each track.
7. Calculate the ratio of the original audio length to the replacment audio length.
8. Use the inverse (reciprocal) of the ratio to adjust the length of the replacement track.
9. Adjust the start of the replacement track to match the original track.
10. Adjust the length of the entire replacement track to match the length of the entire original track.
11. Measure the level of each tracks.
12. Adjust the level of the replacement track to match the original track.
