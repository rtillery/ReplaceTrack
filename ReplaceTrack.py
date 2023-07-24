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
import numpy
import soundfile
import librosa
import sounddevice

gScriptDir = os.path.abspath(os.path.dirname(__file__))

print('gScriptDir: "{}"'.format(gScriptDir))

# TODO: Replace with full file paths obtained from command line
gOrgFile = gScriptDir + "/alex-productions-promotional-video_8bit,32kHz,0.ogg_48kbps.mp3_-12dB,40kbps.wma_+12dB,SnakeEQ,0.ogg_44.1KHz,0.998108143x.wav"
print('gOrgFile: "{}"'.format(gOrgFile))

gReplFile = gScriptDir + "/alex-productions-promotional-video.wav"
print('gReplFile: "{}"'.format(gReplFile))

print('vvvvv Loading gOrgFile vvvvv')

gOrgInfo = soundfile.info(gOrgFile)
print('gOrgInfo: {}'.format(gOrgInfo))
# print('type of gOrgInfo.channels: {}'.format(type(gOrgInfo.channels)))
# print('type of gOrgInfo.samplerate: {}'.format(type(gOrgInfo.samplerate)))

# gOrgData, gOrgSR = librosa.load(gOrgFile)
# gOrgData, gOrgSR = librosa.load(gOrgFile, sr=gOrgInfo.samplerate)
# gOrgData, gOrgSR = librosa.load(gOrgFile, sr=gOrgInfo.samplerate, mono=(gOrgInfo.channels == 1))
gTmpOrgData, gOrgSR = librosa.load(gOrgFile, sr=gOrgInfo.samplerate, mono=(gOrgInfo.channels == 1))
print('gOrgSR: {}'.format(gOrgSR))
print('type of gTmpOrgData: {}'.format(type(gTmpOrgData)))
if isinstance(gTmpOrgData, numpy.ndarray):
    print('gTmpOrdData.ndim: {}'.format(gTmpOrgData.ndim))
    print('gTmpOrgData.shape: {}'.format(gTmpOrgData.shape))

# Rotate array, because it seems to be incompatible as-is with sounddevice
gOrgData = numpy.swapaxes(gTmpOrgData, 0, 1)
if isinstance(gOrgData, numpy.ndarray):
    print('gOrdData.ndim: {}'.format(gOrgData.ndim))
    print('gOrgData.shape: {}'.format(gOrgData.shape))

print('^^^^^ gOrgFile loaded ^^^^^')

# If librosa.load() resamples, g*SR != g*Info.samplerate
sounddevice.play(gOrgData, samplerate=gOrgSR, blocking=True)

print('vvvvv Loading gReplFile vvvvv')

gReplInfo = soundfile.info(gReplFile)
print('gReplInfo: {}'.format(gReplInfo))

gReplData, gReplSR = librosa.load(gReplFile, sr=gReplInfo.samplerate, mono=(gReplInfo.channels == 1))
print('gReplSR: {}'.format(gReplSR))

print('^^^^^ gReplFile loaded ^^^^^')

# If librosa.load() resamples, g*SR != g*Info.samplerate
# sounddevice.play(gReplData, samplerate=gReplSR, blocking=True)
