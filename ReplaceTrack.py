#!/usr/bin/env python3

#
# ReplaceTrack.py
#
# Tool to replace a music track with another, matching the replacement to the
# timing of the first.
#
# This tool was created to replace tracks in rhythm games, like Clone Hero,
# that are corrupted in some way, with a higher quality version. However,
# to maintain compatibility with the timing of the game portion, in a .mid
# (.midi) or .chart file, the replacement track needs to be aligned with the
# timing of the original one.
#

#
# The steps that are intended to follow to accomplish this are:
#
#  1. Detect the start of each track using a silence threshold.
#  2. Use the starts to do a coarse alighment of the tracks by adjusting the
#     start of the replacement track to match the original. (It is assumed
#     that, because the tracks have different sources, a simple silcence
#     threshold will not be enough for fine alignment, which will be done
#     later).
#  3. Adjust the start of the replacement track to match the original
#     coarse value. This may involve cropping the intro silence or extending
#     it with additional silence.
#  4. Detect the end of each track using a silence threshold.
#  5. Use the ends to do a coarse alignment of the tracks by cropping or
#     prepending the replacement track to match the original.
#  6. Calculate the audio length (end - start) of each track.
#  7. Calculate the ratio of the original audio length to the replacment
#     audio length.
#  8. Use the inverse (reciprocal) of the ratio to adjust the length of the
#     replacement track.
#  9. Adjust the start of the replacement track to match the original track.
# 10. Adjust the length of the entire replacement track to match the length of
#     the entire original track.
# 11. Measure the level of each tracks.
# 12. Adjust the level of the replacement track to match the original track.
#

import os
import librosa

gScriptDir = os.path.abspath(os.path.dirname(__file__))

print('gScriptDir: "{}"'.format(gScriptDir))

# TODO: Replace with full file paths obtained from command line
gOrgFile = gScriptDir + "alex-productions-promotional-video_8bit,32kHz,0.ogg_48kbps.mp3_-12dB,40kbps.wma_+12dB,SnakeEQ,0.ogg_44.1KHz,0.998108143x.wav"
gReplFile = gScriptDir + "alex-productions-promotional-video.wav"

print('gOrgFile: "{}"'.format(gOrgFile))
print('gReplFile: "{}"'.format(gReplFile))
