# -*- coding: utf-8 -*-
#
# mididings
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#

"""
Contract tests for the _mididings extension module.

The pure-Python package only talks to the compiled core through _mididings,
so these tests pin down that boundary: which names exist, the numeric values
of the enums (they are bit masks, and are combined and compared as ints on
the Python side), and that every _mididings attribute the package refers to
actually resolves.  Any replacement for the C++ core has to pass these.
"""

import ast
import os
import unittest

import _mididings
import mididings
from mididings import setup, engine
from mididings.event import NoteOnEvent


MIDI_EVENT_TYPES = {
    'NONE': 0, 'NOTEON': 1, 'NOTEOFF': 2, 'NOTE': 3, 'CTRL': 4,
    'PITCHBEND': 8, 'AFTERTOUCH': 16, 'POLY_AFTERTOUCH': 32, 'PROGRAM': 64,
    'SYSEX': 128, 'SYSCM_QFRAME': 256, 'SYSCM_SONGPOS': 512,
    'SYSCM_SONGSEL': 1024, 'SYSCM_TUNEREQ': 2048, 'SYSCM': 3840,
    'SYSRT_CLOCK': 4096, 'SYSRT_START': 8192, 'SYSRT_CONTINUE': 16384,
    'SYSRT_STOP': 32768, 'SYSRT_SENSING': 65536, 'SYSRT_RESET': 131072,
    'SYSRT': 258048, 'SYSTEM': 262016, 'DUMMY': 536870912,
    'ANY': 1073741823,
}

TRANSFORM_MODES = {
    'OFFSET': 1, 'MULTIPLY': 2, 'FIXED': 3, 'GAMMA': 4, 'CURVE': 5,
}

EVENT_ATTRIBUTES = {
    'PORT': -1, 'CHANNEL': -2,
    'DATA1': -3, 'NOTE': -3, 'CTRL': -3,
    'DATA2': -4, 'VELOCITY': -4, 'VALUE': -4, 'PROGRAM': -4,
}

MODULE_NAMES = {
    'BackendBase', 'Call', 'Channel', 'ChannelFilter', 'CtrlCurve',
    'CtrlFilter', 'CtrlMap', 'CtrlRange', 'CtrlValueFilter', 'Engine',
    'EventAttribute', 'Filter', 'Generator', 'InvertedFilter', 'Key',
    'KeyFilter', 'MidiEvent', 'MidiEventType', 'Pass', 'Patch',
    'PitchbendRange', 'Port', 'PortFilter', 'ProgramFilter', 'Sanitize',
    'SceneSwitch', 'SubSceneSwitch', 'SysExFilter', 'SysExGenerator',
    'TransformMode', 'Transpose', 'TypeFilter', 'Unit', 'UnitEx',
    'Velocity', 'VelocityFilter', 'VelocitySlope', 'available_backends',
    'buffer_to_midi_event', 'create_backend', 'midi_event_to_buffer',
    'send_midi',
}

ENGINE_METHODS = {
    'add_scene', 'current_scene', 'current_subscene', 'get_client_id',
    'get_client_name', 'get_client_uuid', 'output_event', 'process_event',
    'set_processing', 'start', 'switch_scene', 'time',
}

# References in the Python package that are known not to resolve.  Each
# entry here is a bug; see the matching expectedFailure test below.
KNOWN_BROKEN_REFERENCES = {
    'Engine.process',
}


def _package_references():
    """
    Yield (dotted name, file, line) for every attribute chain rooted at the
    name _mididings in the mididings package sources, e.g. 'Engine.start'.
    """
    root = os.path.dirname(mididings.__file__)
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if not fn.endswith('.py'):
                continue
            path = os.path.join(dirpath, fn)
            with open(path, encoding='utf-8') as f:
                tree = ast.parse(f.read(), path)
            for node in ast.walk(tree):
                if not isinstance(node, ast.Attribute):
                    continue
                chain = []
                n = node
                while isinstance(n, ast.Attribute):
                    chain.append(n.attr)
                    n = n.value
                if isinstance(n, ast.Name) and n.id == '_mididings':
                    yield '.'.join(reversed(chain)), path, node.lineno


class BindingSurfaceTestCase(unittest.TestCase):

    def test_module_names(self):
        missing = MODULE_NAMES - set(dir(_mididings))
        self.assertFalse(missing, "missing from _mididings: %s" % missing)

    def test_engine_methods(self):
        missing = ENGINE_METHODS - set(dir(_mididings.Engine))
        self.assertFalse(missing, "missing from Engine: %s" % missing)

    def test_enum_values(self):
        for enum, expected in ((_mididings.MidiEventType, MIDI_EVENT_TYPES),
                               (_mididings.TransformMode, TRANSFORM_MODES),
                               (_mididings.EventAttribute, EVENT_ATTRIBUTES)):
            for name, value in expected.items():
                self.assertEqual(int(getattr(enum, name)), value,
                                 "%s.%s" % (enum.__name__, name))

    def test_enum_names_mapping(self):
        # constants.py builds the public constants from .names
        names = _mididings.MidiEventType.names
        self.assertEqual({k: int(v) for k, v in names.items()},
                         MIDI_EVENT_TYPES)

    def test_event_type_masks(self):
        t = MIDI_EVENT_TYPES
        self.assertEqual(t['NOTE'], t['NOTEON'] | t['NOTEOFF'])
        self.assertEqual(t['SYSCM'], t['SYSCM_QFRAME'] | t['SYSCM_SONGPOS']
                         | t['SYSCM_SONGSEL'] | t['SYSCM_TUNEREQ'])
        self.assertEqual(t['SYSRT'], t['SYSRT_CLOCK'] | t['SYSRT_START']
                         | t['SYSRT_CONTINUE'] | t['SYSRT_STOP']
                         | t['SYSRT_SENSING'] | t['SYSRT_RESET'])
        self.assertEqual(t['SYSTEM'], t['SYSEX'] | t['SYSCM'] | t['SYSRT'])
        # every concrete type is a single distinct bit covered by ANY
        concrete = [v for k, v in t.items()
                    if k not in ('NONE', 'NOTE', 'SYSCM', 'SYSRT', 'SYSTEM',
                                 'ANY', 'DUMMY')]
        for v in concrete:
            self.assertEqual(bin(v).count('1'), 1)
            self.assertEqual(t['ANY'] & v, v)
        self.assertEqual(len(set(concrete)), len(concrete))

    def test_midi_event_defaults(self):
        ev = _mididings.MidiEvent()
        self.assertEqual((int(ev.type_), ev.port_, ev.channel_,
                          ev.data1, ev.data2), (0, 0, 0, 0, 0))

    def test_midi_event_fields_are_independent(self):
        ev = _mididings.MidiEvent()
        ev.port_ = 1
        ev.channel_ = 2
        ev.data1 = 3
        ev.data2 = 4
        self.assertEqual((ev.port_, ev.channel_, ev.data1, ev.data2),
                         (1, 2, 3, 4))

    def test_midi_event_int_ranges(self):
        # pitchbend values are negative, port numbers can be large
        ev = _mididings.MidiEvent()
        ev.data2 = -8192
        self.assertEqual(ev.data2, -8192)
        ev.port_ = 65535
        self.assertEqual(ev.port_, 65535)

    def test_dummy_backend(self):
        self.assertIsNone(_mididings.create_backend('dummy', 'x', [], []))

    def test_unknown_backend(self):
        with self.assertRaises(Exception):
            _mididings.create_backend('no-such-backend', 'x', [], [])

    def test_package_references_resolve(self):
        missing = set()
        for ref, path, line in _package_references():
            obj = _mididings
            try:
                for part in ref.split('.'):
                    obj = getattr(obj, part)
            except AttributeError:
                if ref not in KNOWN_BROKEN_REFERENCES:
                    missing.add('%s (%s:%d)' % (ref, path, line))
        self.assertFalse(missing, "unresolved _mididings references:\n"
                                  + "\n".join(sorted(missing)))

    @unittest.expectedFailure
    def test_engine_process(self):
        # mididings.engine.Engine.process() calls _mididings.Engine.process,
        # which the extension does not expose.
        setup.reset()
        setup.config(data_offset=0, silent=True)
        setup._config_impl(backend='dummy')
        e = engine.Engine()
        try:
            e.setup({0: mididings.Pass()}, None, None, None)
            e.process(NoteOnEvent(0, 0, 60, 100))
        finally:
            # Engine.setup() registers a global weak reference and disables
            # the garbage collector, so this engine would otherwise stay
            # "active" for later tests (see test_engine.test_active)
            engine._TheEngine = None
