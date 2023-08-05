#!/usr/bin/env python3

# Copyright (c) 2023, Rick Tillery. All rights reserved.
# Licensed under the Open Software License version 3.0.

#
# ReplaceTrack.py
#
# Tool to replace audio track with another, matching the original timing,
# duration, and level.
#
# This tool was created to replace tracks in rhythm games, like Clone Hero,
# that are corrupted in some way, with a higher quality version. However, to
# maintain compatibility with the timing of the game portion, in a .mid
# (.midi) or .chart file, the replacement track needs to match the timing of
# the original one.
#
#
# WIP
#
# This tool is a work in progress. At present, the intended approach is:
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
import argparse
from pathlib import Path
from pathlib import PurePath

import numpy
import soundfile
import librosa
import sounddevice

import cProfile

# File and directory naming conventions:
#
# path: (directory containing file or directory itself) /foo/bar, ./, ../bar
#
# file: file (or dir) handle
# dir: dir handle
#
# filename: myfile.ext
# filepath: /foo/bar/myfile.ext, myfile.ext (./myfile.ext), ../bar/myfile.ext
# filedir: /foo/bar, ./, ../bar

class CmdLineParser(argparse.ArgumentParser):
    def __init__(self, **kwargs):
            super().__init__(
                **kwargs,
                description=(
                    'Replace a distorted audio track with another '
                    '(presumbably higher quality version), modifying the '
                    'replacement to match the sample rate, timing, duration, '
                    'level and file format of the orginal.'
                )
            )
            self.add_argument(
                'originalFilepath',
                type=self.AbsPath,
                help='original audio file to be replaced'
            )
            self.add_argument(
                'referenceFilepath',
                type=self.AbsPath,
                help='audio file used to create replacement file'
            )
            self.add_argument(
                'replacementFilepath',
                type=self.AbsPath,
                help='resulting replacement file'
            )

    def AbsPath(self, path):
        return Path(path).resolve()

    def GetArgs(self):
        return self.parse_args()


class SoundFile:
    def __init__(self, filename):
        self.filename = filename
        self.info = soundfile.info(self.filename)
        # TODO: Can tmpData be removed in favor of replacing the data when rotating?
        self.tmpData, self.sampleRate = librosa.load(self.filename,
                                                     sr=self.info.samplerate,
                                                     mono=(self.info.channels == 1))
        # Rotate the data array, because it isn't compatible with sounddevice
        self.data = numpy.swapaxes(self.tmpData, 0, 1)


gArgs = CmdLineParser().GetArgs()

print(gArgs)

print('vvvvv Loading gOrgFile vvvvv')
gOrgFile = SoundFile(gArgs.originalFilepath)
print('gOrgFile: {}'.format(gOrgFile))
print('gOrgFile.info: {}'.format(gOrgFile.info))
print('gOrgFile.sampleRate: {}'.format(gOrgFile.sampleRate))

if isinstance(gOrgFile.data, numpy.ndarray):
    print('gOrdFile.data.ndim: {}'.format(gOrgFile.data.ndim))
    print('gOrgFile.data.shape: {}'.format(gOrgFile.data.shape))

print('^^^^^ gOrgFile loaded ^^^^^')

# If librosa.load() resamples, g*SR != g*Info.samplerate
sounddevice.play(gOrgFile.data, samplerate=gOrgFile.sampleRate, blocking=True)

exit()







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
