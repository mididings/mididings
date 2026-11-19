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
MidiEvent value semantics (pickling, hashing, copying) and conversion
between events and raw MIDI byte buffers.
"""

from tests.helpers import *

from mididings import *
from mididings.event import *

import _mididings

import copy
import pickle


def all_event_kinds():
    return [
        NoteOnEvent(0, 0, 60, 100),
        NoteOffEvent(3, 15, 0, 0),
        CtrlEvent(1, 2, 127, 127),
        PitchbendEvent(0, 0, -8192),
        PitchbendEvent(0, 0, 8191),
        AftertouchEvent(0, 9, 64),
        PolyAftertouchEvent(0, 9, 60, 64),
        ProgramEvent(0, 0, 127),
        SysExEvent(0, b'\xf0\x7e\x7f\x06\x01\xf7'),
        MidiEvent(SYSCM_QFRAME, 0, 0, 0x35, 0),
        MidiEvent(SYSCM_SONGPOS, 0, 0, 0x01, 0x02),
        MidiEvent(SYSCM_SONGSEL, 0, 0, 5, 0),
        MidiEvent(SYSCM_TUNEREQ, 0, 0, 0, 0),
        MidiEvent(SYSRT_CLOCK, 0, 0, 0, 0),
        MidiEvent(SYSRT_START, 0, 0, 0, 0),
        MidiEvent(SYSRT_CONTINUE, 0, 0, 0, 0),
        MidiEvent(SYSRT_STOP, 0, 0, 0, 0),
        MidiEvent(SYSRT_SENSING, 0, 0, 0, 0),
        MidiEvent(SYSRT_RESET, 0, 0, 0, 0),
    ]


class EventSemanticsTestCase(MididingsTestCase):

    def setUp(self):
        MididingsTestCase.setUp(self)
        config(silent=True)

    def test_pickle_all_kinds(self):
        for ev in all_event_kinds():
            for proto in range(pickle.HIGHEST_PROTOCOL + 1):
                r = pickle.loads(pickle.dumps(ev, proto))
                self.assertEqual(r, ev, "%r (protocol %d)" % (ev, proto))
                self.assertIs(type(r), type(ev))

    @data_offsets
    def test_pickle_respects_data_offset(self, off):
        ev = NoteOnEvent(off(2), off(3), 60, 100)
        r = pickle.loads(pickle.dumps(ev))
        self.assertEqual((r.port_, r.channel_), (2, 3))
        self.assertEqual((r.port, r.channel), (off(2), off(3)))

    def test_pickle_after_engine(self):
        # events coming out of the engine must be picklable too
        (r,) = run_engine({0: Pass()}, all_event_kinds()[:1])
        r2 = pickle.loads(pickle.dumps(r[0]))
        self.assertEqual(r2, r[0])

    def test_equality_covers_all_fields(self):
        base = NoteOnEvent(0, 0, 60, 100)
        for other in (NoteOffEvent(0, 0, 60, 100), NoteOnEvent(1, 0, 60, 100),
                      NoteOnEvent(0, 1, 60, 100), NoteOnEvent(0, 0, 61, 100),
                      NoteOnEvent(0, 0, 60, 101)):
            self.assertNotEqual(base, other)
            self.assertTrue(base != other)
            self.assertFalse(base == other)

    def test_equality_sysex_content(self):
        a = SysExEvent(0, b'\xf0\x01\x02\xf7')
        self.assertEqual(a, SysExEvent(0, b'\xf0\x01\x02\xf7'))
        self.assertNotEqual(a, SysExEvent(0, b'\xf0\x01\x03\xf7'))
        self.assertNotEqual(a, SysExEvent(0, b'\xf0\x01\x02\x03\xf7'))

    def test_equality_with_other_types(self):
        ev = NoteOnEvent(0, 0, 60, 100)
        self.assertNotEqual(ev, None)
        self.assertNotEqual(ev, 60)
        self.assertNotEqual(ev, (0, 0, 60, 100))

    @unittest.expectedFailure
    def test_hash_consistent_with_eq(self):
        # equal events must hash equally, otherwise sets and dict keys of
        # events silently hold duplicates.  __hash__ currently falls back to
        # object identity.
        a = NoteOnEvent(0, 0, 60, 100)
        b = NoteOnEvent(0, 0, 60, 100)
        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))
        self.assertEqual(len({a, b}), 1)

    def test_copy_scalar_fields_independent(self):
        a = NoteOnEvent(0, 0, 60, 100)
        b = copy.copy(a)
        b.note = 61
        b.channel = 3
        self.assertEqual(a.note, 60)
        self.assertEqual(a.channel, 0)

    def test_deepcopy_sysex_independent(self):
        for a in (SysExEvent(0, b'\xf0\x01\x02\xf7'),
                  run_engine({0: Pass()},
                             [SysExEvent(0, b'\xf0\x01\x02\xf7')])[0][0]):
            b = copy.deepcopy(a)
            b.sysex[1] = 0x05
            self.assertEqual(a.sysex[1], 0x01)
            self.assertEqual(b.sysex[1], 0x05)

    def test_sysex_in_place_modification_sticks(self):
        # ev.sysex returns a bytearray that is written back when the event
        # is used again; Process() functions rely on this
        (r,) = run_engine({0: Pass()}, [SysExEvent(0, b'\xf0\x01\x02\xf7')])
        ev = r[0]
        ev.sysex[1] = 0x09
        self.assertEqual(ev.sysex[1], 0x09)
        (r2,) = run_engine({0: Pass()}, [ev])
        self.assertEqual(r2[0].sysex, bytearray(b'\xf0\x09\x02\xf7'))

    def test_sysex_assignment_does_not_affect_copy(self):
        a = SysExEvent(0, b'\xf0\x01\x02\xf7')
        b = copy.copy(a)
        b.sysex = b'\xf0\x05\xf7'
        self.assertEqual(a.sysex, bytearray(b'\xf0\x01\x02\xf7'))

    def test_repr_roundtrip_all_kinds(self):
        for ev in all_event_kinds():
            self.assertEqual(eval(repr(ev), self.mididings_dict), ev)

    def test_wrong_type_attribute_access(self):
        with self.assertRaises(AttributeError):
            CtrlEvent(0, 0, 1, 1).note
        with self.assertRaises(AttributeError):
            NoteOnEvent(0, 0, 1, 1).sysex
        with self.assertRaises(AttributeError):
            MidiEvent(SYSRT_CLOCK, 0, 0, 0, 0).value


class BufferConversionTestCase(unittest.TestCase):
    """
    _mididings.buffer_to_midi_event() / midi_event_to_buffer(), used by
    process_file() for standard MIDI files, and mirroring what the ALSA and
    JACK backends do with live input.
    """

    ROUNDTRIP = [
        [0x90, 60, 100],
        [0x8f, 0, 0],
        [0xb3, 7, 127],
        [0xe0, 0, 0],               # pitchbend minimum
        [0xe0, 0x00, 0x40],         # pitchbend centre
        [0xe5, 0x7f, 0x7f],         # pitchbend maximum
        [0xd2, 64],
        [0xa1, 60, 64],
        [0xc9, 127],
        [0xf0, 0x7e, 0x7f, 0x06, 0x01, 0xf7],
        [0xf1, 0x35],
        [0xf2, 0x01, 0x02],
        [0xf3, 5],
        [0xf6],
        [0xf8], [0xfa], [0xfb], [0xfc], [0xfe], [0xff],
    ]

    def test_roundtrip(self):
        for buf in self.ROUNDTRIP:
            ev = _mididings.buffer_to_midi_event(buf, 3, 12345)
            out, port, frame = _mididings.midi_event_to_buffer(ev)
            self.assertEqual(list(out), buf, "buffer %r" % buf)
            self.assertEqual((port, frame), (3, 12345))

    def test_noteon_velocity_zero_becomes_noteoff(self):
        ev = _mididings.buffer_to_midi_event([0x93, 60, 0], 0, 0)
        self.assertEqual(int(ev.type_), int(NOTEOFF))
        self.assertEqual((ev.channel_, ev.data1, ev.data2), (3, 60, 0))

    def test_pitchbend_values(self):
        for buf, value in (([0xe0, 0, 0], -8192), ([0xe0, 0, 0x40], 0),
                           ([0xe0, 0x7f, 0x7f], 8191),
                           ([0xe0, 0x01, 0x40], 1)):
            ev = _mididings.buffer_to_midi_event(buf, 0, 0)
            self.assertEqual(ev.data2, value)

    def test_large_frame(self):
        # frame is uint64 (SMF pulses / JACK frames can exceed 32 bits)
        frame = 2 ** 40 + 7
        ev = _mididings.buffer_to_midi_event([0x90, 1, 2], 0, frame)
        self.assertEqual(_mididings.midi_event_to_buffer(ev)[2], frame)

    def test_unknown_status_byte(self):
        for buf in ([0xf4], [0xf5], [0xf9], [0xfd]):
            ev = _mididings.buffer_to_midi_event(buf, 0, 0)
            self.assertEqual(int(ev.type_), int(NONE))
            self.assertEqual(len(_mididings.midi_event_to_buffer(ev)[0]), 0)

    def test_sysex_256_bytes(self):
        buf = [0xf0] + [0x01] * 254 + [0xf7]
        ev = _mididings.buffer_to_midi_event(buf, 0, 0)
        self.assertEqual(list(_mididings.midi_event_to_buffer(ev)[0]), buf)

    @unittest.expectedFailure
    def test_sysex_longer_than_256_bytes(self):
        # midi_event_to_buffer() uses a fixed 256-byte buffer and silently
        # returns an empty buffer for longer sysex, so process_file() drops
        # e.g. patch dumps from MIDI files
        buf = [0xf0] + [0x01] * 1000 + [0xf7]
        ev = _mididings.buffer_to_midi_event(buf, 0, 0)
        self.assertEqual(list(_mididings.midi_event_to_buffer(ev)[0]), buf)

    @unittest.expectedFailure
    def test_truncated_buffer_rejected(self):
        # status bytes are read without checking the length, so a truncated
        # message reads past the end of the buffer (garbage data bytes)
        with self.assertRaises(ValueError):
            _mididings.buffer_to_midi_event([0x90], 0, 0)

    @unittest.expectedFailure
    def test_empty_buffer_does_not_crash(self):
        # an empty buffer dereferences vector::front() and segfaults
        p = run_isolated("""
            import _mididings
            try:
                _mididings.buffer_to_midi_event([], 0, 0)
            except Exception:
                pass
            print('ok')
        """)
        self.assertIsNotNone(p, 'timed out')
        self.assertEqual(p.returncode, 0, p.stderr)
