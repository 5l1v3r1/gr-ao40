#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# gr-ao40 GNU Radio OOT module for AO-40 FEC
# 
# Copyright 2017 Daniel Estevez <daniel@destevez.net>
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from construct import *

SatID = Enum(BitsInteger(2),\
                  FC1EM = 0,\
                  FC2 = 1,\
                  FC1FM = 2,\
                  extended = 3)

FrameType = Enum(BitsInteger(6),\
    WO1 = 0,\
    WO2 = 1,\
    WO3 = 2,\
    WO4 = 3,\
    WO5 = 4,\
    WO6 = 5,\
    WO7 = 6,\
    WO8 = 7,\
    WO9 = 8,\
    WO10 = 9,\
    WO11 = 10,\
    WO12 = 11,\
    HR1 = 12,\
    FM1 = 13,\
    FM2 = 14,\
    FM3 = 15,\
    HR2 = 16,\
    FM4 = 17,\
    FM5 = 18,\
    FM6 = 19,\
    HR3 = 20,\
    FM7 = 21,\
    FM8 = 22,\
    FM9 = 23)

class FrameTypeAdapter(Adapter):
    def _encode(self, obj, context):
        return obj.value
    def _decode(self, obj, context):
        return FrameType(obj)

FrameTypeField = FrameTypeAdapter(BitsInteger(6))

Header = BitStruct(
    'satid' / SatID,
    'frametype' / FrameType,
    )

EPS = Struct(
    'photovoltage' / BitsInteger(16)[3],
    'photocurrent' / BitsInteger(16),
    'batteryvoltage' / BitsInteger(16),
    'systemcurrent' / BitsInteger(16),
    'rebootcount' / BitsInteger(16),
    'softwareerrors' / BitsInteger(16),
    'boostconvertertemp' / Octet[3],
    'batterytemp' / Octet,
    'latchupcount5v' / Octet,
    'latchupcount3v3' / Octet,
    'resetcause' / Octet,
    'MPPTmode' / Octet,
    )

BOB = Struct(
    'sunsensor' / BitsInteger(10)[3],
    'paneltemp' / BitsInteger(10)[4],
    '3v3voltage' / BitsInteger(10),
    '3v3current' / BitsInteger(10),
    '5voltage' / BitsInteger(10),
)

RF = Struct(
    'rxdoppler' / Octet,
    'rxrssi' / Octet,
    'temp' / Octet,
    'rxcurrent' / Octet,
    'tx3v3current' / Octet,
    'tx5vcurrent' / Octet,
    )

PA = Struct(
    'revpwr' / Octet,
    'fwdpwr' / Octet,
    'boardtemp' / Octet,
    'boardcurr' / Octet,
    )

Ants = Struct(
    'temp' / Octet[2],
    'deployment' / Flag[4],
    )

SW = Struct(
    'seqnumber' / BitsInteger(24),
    'dtmfcmdcount' / BitsInteger(6),
    'dtmflastcmd' / BitsInteger(5),
    'dtmfcmdsuccess' / Flag,
    'datavalid' / Flag[7],
    'eclipse' / Flag,
    'safemode' / Flag,
    'hwabf' / Flag,
    'swabf' / Flag,
    'deploymentwait' / Flag,
    )

RealTime = BitStruct(
    'eps' / EPS,
    'bob' / BOB,
    'rf' / RF,
    'pa' / PA,
    'ants' / Ants,
    'sw' / SW,
    )

Frame = Struct(
    Embedded(Header),
    'realtime' / RealTime,
    'payload' / Bytes(200),
    )

FitterMessage = String(200)

def beacon_parse(data):
    return Frame.parse(data)
