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
Boundary values and common pitfalls for filters, modifiers and generators.
"""

from tests.helpers import *

from mididings import *
from mididings.event import *


class UnitEdgeCaseTestCase(MididingsTestCase):

    def setUp(self):
        MididingsTestCase.setUp(self)
        config(silent=True)

    def out(self, patch, ev):
        (r,) = run_engine({0: patch}, [ev])
        return r

    def outs(self, patch, events):
        return run_engine({0: patch}, events)

    def velocities(self, patch, values):
        r = self.outs(patch, [NoteOnEvent(0, 0, 60, v) for v in values])
        return [x[0].velocity for x in r]

    def ctrl_values(self, patch, values, ctrl=1):
        r = self.outs(patch, [CtrlEvent(0, 0, ctrl, v) for v in values])
        return [x[0].value for x in r]

    # --- filters must not cause stuck notes ------------------------------

    def test_velocity_filter_passes_noteoffs(self):
        # note-offs must get through a velocity filter, whatever their
        # release velocity, or notes would hang
        for vel in (0, 64, 127):
            self.assertEqual(
                self.out(VelocityFilter(100, 110), NoteOffEvent(0, 0, 60, vel)),
                [NoteOffEvent(0, 0, 60, vel)])

    def test_key_filter_applies_to_noteoffs(self):
        f = KeyFilter(60, 62)
        self.assertEqual(len(self.out(f, NoteOffEvent(0, 0, 60, 0))), 1)
        self.assertEqual(len(self.out(f, NoteOffEvent(0, 0, 62, 0))), 0)

    def test_key_filter_range_is_half_open(self):
        f = KeyFilter(60, 62)
        self.assertEqual([bool(self.out(f, NoteOnEvent(0, 0, n, 1)))
                          for n in (59, 60, 61, 62)],
                         [False, True, True, False])

    def test_note_filters_pass_other_types(self):
        for f in (KeyFilter(60), VelocityFilter(100), KeyFilter(notes=[])):
            for ev in (CtrlEvent(0, 0, 1, 1), ProgramEvent(0, 0, 5),
                       PitchbendEvent(0, 0, 100)):
                self.assertEqual(self.out(f, ev), [ev], "%r %r" % (f, ev))

    def test_key_filter_empty_list_blocks_notes(self):
        self.assertEqual(self.out(KeyFilter(notes=[]),
                                  NoteOnEvent(0, 0, 60, 1)), [])

    def test_type_filter_note_matches_on_and_off(self):
        f = Filter(NOTE)
        self.assertTrue(self.out(f, NoteOnEvent(0, 0, 1, 1)))
        self.assertTrue(self.out(f, NoteOffEvent(0, 0, 1, 1)))
        self.assertFalse(self.out(f, CtrlEvent(0, 0, 1, 1)))

    def test_sysex_filter_exact_vs_prefix(self):
        exact = SysExFilter(b'\xf0\x41\x02\xf7')
        prefix = SysExFilter(b'\xf0\x41')
        msgs = (b'\xf0\x41\x02\xf7', b'\xf0\x41\x02\x03\xf7',
                b'\xf0\x41\xf7', b'\xf0\x42\x02\xf7')
        self.assertEqual([bool(self.out(exact, SysExEvent(0, m)))
                          for m in msgs], [True, False, False, False])
        self.assertEqual([bool(self.out(prefix, SysExEvent(0, m)))
                          for m in msgs], [True, True, True, False])

    def test_sysex_filter_manufacturer(self):
        f = SysExFilter(manufacturer=0x41)
        self.assertTrue(self.out(f, SysExEvent(0, b'\xf0\x41\x02\xf7')))
        # 0x41 appearing later in a 3-byte manufacturer id is not a match
        self.assertFalse(self.out(f, SysExEvent(0, b'\xf0\x00\x00\x41\xf7')))

    # --- modifiers at the edges ----------------------------------------

    def test_transpose_out_of_range_dropped(self):
        self.assertEqual(self.out(Transpose(-61), NoteOnEvent(0, 0, 60, 1)),
                         [])
        self.assertEqual(self.out(Transpose(68), NoteOnEvent(0, 0, 60, 1)),
                         [])
        self.assertEqual(self.out(Transpose(67), NoteOnEvent(0, 0, 60, 1)),
                         [NoteOnEvent(0, 0, 127, 1)])

    def test_transpose_ignores_non_notes(self):
        ev = CtrlEvent(0, 0, 60, 64)
        self.assertEqual(self.out(Transpose(5), ev), [ev])

    def test_transpose_moves_poly_aftertouch_with_notes(self):
        # poly aftertouch refers to a key, so it must follow the transposed
        # note or the pressure goes to the wrong (or no) sounding note
        self.assertEqual(self.out(Transpose(5),
                                  PolyAftertouchEvent(0, 0, 60, 64)),
                         [PolyAftertouchEvent(0, 0, 65, 64)])

    def test_velocity_ignores_noteoffs(self):
        ev = NoteOffEvent(0, 0, 60, 100)
        self.assertEqual(self.out(Velocity(fixed=50), ev), [ev])

    def test_velocity_gamma_and_curve_keep_notes_audible(self):
        # gamma and curve never map a positive velocity to 0 (which would
        # turn the note-on into a note-off)
        for patch in (Velocity(gamma=0.1), Velocity(gamma=10),
                      Velocity(curve=-10), Velocity(curve=10)):
            vs = self.velocities(patch, range(1, 128))
            self.assertTrue(all(1 <= v <= 127 for v in vs), repr(patch))
            self.assertEqual(vs, sorted(vs), "not monotonic: %r" % patch)

    def test_velocity_gamma_and_curve_endpoints(self):
        for patch in (Velocity(gamma=0.5), Velocity(gamma=2),
                      Velocity(curve=-3), Velocity(curve=3)):
            self.assertEqual(self.velocities(patch, [127]), [127])

    def test_velocity_curve_zero_is_identity(self):
        self.assertEqual(self.velocities(Velocity(curve=0), range(1, 128)),
                         list(range(1, 128)))

    @unittest.expectedFailure
    def test_velocity_gamma_must_be_positive(self):
        # gamma=0 divides by zero and negative gamma inverts the curve;
        # neither is rejected at patch construction time
        for gamma in (0, -1):
            with self.assertRaises(ValueError):
                Velocity(gamma=gamma)

    def test_velocity_slope_clamps_outside_notes(self):
        p = VelocitySlope(notes=(40, 80), offset=(-10, 10))
        self.assertEqual([self.out(p, NoteOnEvent(0, 0, n, 64))[0].velocity
                          for n in (0, 40, 60, 80, 127)],
                         [54, 54, 64, 74, 74])

    def test_velocity_slope_needs_two_notes(self):
        with self.assertRaises(ValueError):
            VelocitySlope(notes=(60,), offset=(1,))

    def test_ctrl_range_endpoints(self):
        p = CtrlRange(1, 10, 20)
        self.assertEqual(self.ctrl_values(p, (0, 127)), [10, 20])

    def test_ctrl_range_identity(self):
        p = CtrlRange(1, 0, 127)
        self.assertEqual(self.ctrl_values(p, range(128)), list(range(128)))

    def test_ctrl_range_is_monotonic(self):
        p = CtrlRange(1, 20, 100, 30, 90)
        vs = self.ctrl_values(p, range(128))
        self.assertEqual(vs, sorted(vs))
        self.assertEqual((vs[0], vs[30], vs[90], vs[127]), (20, 20, 100, 100))

    def test_ctrl_range_other_controllers_untouched(self):
        ev = CtrlEvent(0, 0, 2, 64)
        self.assertEqual(self.out(CtrlRange(1, 0, 10), ev), [ev])

    def test_ctrl_map_to_same_controller(self):
        ev = CtrlEvent(0, 0, 7, 1)
        self.assertEqual(self.out(CtrlMap(7, 7), ev), [ev])

    def test_pitchbend_range_extremes(self):
        p = PitchbendRange(-12, 12, range=12)
        self.assertEqual(self.out(p, PitchbendEvent(0, 0, -8192))[0].value,
                         -8192)
        self.assertEqual(self.out(p, PitchbendEvent(0, 0, 8191))[0].value,
                         8191)
        self.assertEqual(self.out(p, PitchbendEvent(0, 0, 0))[0].value, 0)

    def test_pitchbend_range_sign_preserved(self):
        p = PitchbendRange(-2, 2)
        for v in (-8192, -4096, -1, 1, 4096, 8191):
            r = self.out(p, PitchbendEvent(0, 0, v))[0].value
            self.assertTrue(r * v >= 0, "%d -> %d" % (v, r))

    # --- generators ------------------------------------------------------

    def test_generator_takes_values_from_event(self):
        self.assertEqual(
            self.out(Ctrl(EVENT_NOTE, EVENT_VELOCITY), NoteOnEvent(0, 0, 10, 20)),
            [CtrlEvent(0, 0, 10, 20)])
        self.assertEqual(
            self.out(NoteOn(EVENT_CTRL, EVENT_VALUE), CtrlEvent(0, 3, 10, 20)),
            [NoteOnEvent(0, 3, 10, 20)])

    def test_generator_keeps_port_and_channel(self):
        self.assertEqual(self.out(Ctrl(7, 1), NoteOnEvent(2, 5, 60, 1)),
                         [CtrlEvent(2, 5, 7, 1)])

    def test_sysex_generator(self):
        self.assertEqual(self.out(SysEx(b'\xf0\x01\xf7'),
                                  NoteOnEvent(0, 0, 1, 1)),
                         [SysExEvent(0, b'\xf0\x01\xf7')])

    # --- argument handling ----------------------------------------------

    def test_out_of_range_arguments_rejected(self):
        for f in (lambda: Channel(16), lambda: Channel(-1),
                  lambda: Key(128), lambda: CtrlFilter(128),
                  lambda: NoteOnEvent(0, 0, 128, 1)):
            with self.assertRaises(ValueError):
                f()

    def test_overload_mismatch_raises_type_error(self):
        with self.assertRaises(TypeError):
            SysExFilter(b'\xf0\x01', bogus=True)

    @unittest.expectedFailure
    def test_overload_mismatch_message(self):
        # building the "no suitable overload" message crashes because
        # misc.formatargspec() (the Python 3.11 replacement for
        # inspect.formatargspec) doesn't accept formatvalue=, so users get
        # an unrelated TypeError instead of the list of candidates
        with self.assertRaisesRegex(TypeError, 'no suitable overload'):
            SysExFilter(b'\xf0\x01', bogus=True)
