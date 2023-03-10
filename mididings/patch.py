# -*- coding: utf-8 -*-
#
# mididings
#
# Copyright (C) 2008-2014  Dominic Sacré  <dominic.sacre@gmx.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#

import _mididings

import mididings.units as _units
import mididings.constants as _constants


class Patch(_mididings.Patch):
    def __init__(self, p):
        _mididings.Patch.__init__(self, self.build(p))

    def build(self, p):
        if isinstance(p, _units.base._Chain):
            return Patch.Chain(self.build(i) for i in p)

        elif isinstance(p, list):
            gen = (self.build(i) for i in p)

            remove_duplicates = True
            if hasattr(p, 'remove_duplicates'):
                remove_duplicates = (p.remove_duplicates != False)

            return Patch.Fork(gen, remove_duplicates)

        elif isinstance(p, dict):
            return self.build(
                _units.splits._make_split(_units.base.Filter, p, unpack=True)
            )

        elif isinstance(p, _units.init._InitExit):
            return Patch.Single(_mididings.Pass(False))

        elif isinstance(p, _units.base._Unit):
            if isinstance(p.unit, _mididings.Unit):
                return Patch.Single(p.unit)
            elif isinstance(p.unit, _mididings.UnitEx):
                return Patch.Extended(p.unit)

        elif isinstance(p, _constants._EventType):
            return Patch.Single(_mididings.TypeFilter(p))

        raise TypeError(f"type '{type(p).__name__}' not allowed in patch. offending object is: {p!r}")


def get_init_patches(patch):
    if isinstance(patch, _units.base._Chain):
        return flatten([get_init_patches(p) for p in patch])

    elif isinstance(patch, list):
        return flatten([get_init_patches(p) for p in patch])

    elif isinstance(patch, dict):
        return flatten([get_init_patches(p) for p in patch.values()])

    elif isinstance(patch, _units.init._InitExit):
        return [patch.init_patch]

    else:
        return []


def get_exit_patches(patch):
    if isinstance(patch, _units.base._Chain):
        return flatten([get_exit_patches(p) for p in patch])

    elif isinstance(patch, list):
        return flatten([get_exit_patches(p) for p in patch])

    elif isinstance(patch, dict):
        return flatten([get_exit_patches(p) for p in patch.values()])

    elif isinstance(patch, _units.init._InitExit):
        return [patch.exit_patch]

    else:
        return []


def flatten(patch):
    r = []
    for i in patch:
        if isinstance(i, list) and not isinstance(i, _units.base._Chain):
            r.extend(i)
        else:
            r.append(i)
    return r
