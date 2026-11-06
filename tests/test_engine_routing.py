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
Engine behaviour across event sequences: note-off and sustain routing after
scene switches, init/exit patches, subscenes, control/pre/post ordering, and
the final sanitize step.
"""

from tests.helpers import *

from mididings import *
from mididings.event import *


PROGRAM_SWITCH = Filter(PROGRAM) >> SceneSwitch()


class EngineRoutingTestCase(MididingsTestCase):

    def setUp(self):
        MididingsTestCase.setUp(self)
        config(silent=True)

    # --- note-off / sustain routing -------------------------------------

    def test_noteoff_follows_noteon_scene(self):
        # a note-off must go through the patch that handled its note-on,
        # otherwise switching scenes while holding a note leaves it stuck
        r = run_engine({0: Transpose(12), 1: Transpose(24)}, [
            NoteOnEvent(0, 0, 60, 100),
            ProgramEvent(0, 0, 1),
            NoteOffEvent(0, 0, 60, 0),
            NoteOnEvent(0, 0, 60, 100),
            NoteOffEvent(0, 0, 60, 0),
        ], control=PROGRAM_SWITCH)
        self.assertEqual(r[2], [NoteOffEvent(0, 0, 72, 0)])
        self.assertEqual(r[3], [NoteOnEvent(0, 0, 84, 100)])
        self.assertEqual(r[4], [NoteOffEvent(0, 0, 84, 0)])

    def test_noteoff_routing_is_per_port_channel_note(self):
        r = run_engine({0: Transpose(12), 1: Transpose(24)}, [
            NoteOnEvent(0, 0, 60, 100),
            ProgramEvent(0, 0, 1),
            NoteOffEvent(0, 1, 60, 0),      # other channel
            NoteOffEvent(1, 0, 60, 0),      # other port
            NoteOffEvent(0, 0, 61, 0),      # other note
            NoteOffEvent(0, 0, 60, 0),      # the held note
        ], control=PROGRAM_SWITCH)
        self.assertEqual(r[2], [NoteOffEvent(0, 1, 84, 0)])
        self.assertEqual(r[3], [NoteOffEvent(1, 0, 84, 0)])
        self.assertEqual(r[4], [NoteOffEvent(0, 0, 85, 0)])
        self.assertEqual(r[5], [NoteOffEvent(0, 0, 72, 0)])

    def test_noteoff_routing_high_port_numbers(self):
        # the routing key packs port, channel and note into one integer;
        # make sure large port numbers don't collide with channels/notes
        r = run_engine({0: Transpose(12), 1: Transpose(24)}, [
            NoteOnEvent(0, 0, 60, 100),
            ProgramEvent(0, 0, 1),
            NoteOffEvent(1 << 16, 0, 60, 0),
            NoteOffEvent(0, 0, 60, 0),
        ], control=PROGRAM_SWITCH)
        self.assertEqual(r[3], [NoteOffEvent(0, 0, 72, 0)])

    def test_retriggered_note_across_switch(self):
        # the same note is struck in two scenes before either is released.
        # both note-offs must be produced, one per transposition.
        r = run_engine({0: Transpose(12), 1: Transpose(24)}, [
            NoteOnEvent(0, 0, 60, 100),
            ProgramEvent(0, 0, 1),
            NoteOnEvent(0, 0, 60, 100),
            NoteOffEvent(0, 0, 60, 0),
            NoteOffEvent(0, 0, 60, 0),
        ], control=PROGRAM_SWITCH)
        offs = sorted(ev.note for ev in r[3] + r[4])
        self.assertEqual(offs, [72, 84])

    @unittest.expectedFailure
    def test_noteon_velocity_zero_is_a_noteoff(self):
        # MIDI treats note-on with velocity 0 as note-off.  The backends
        # convert it when reading raw MIDI, but events created in Python
        # (Process(), process_event()) skip that, so the held note is
        # routed through the new scene and stays stuck in the old one.
        r = run_engine({0: Transpose(12), 1: Transpose(24)}, [
            NoteOnEvent(0, 0, 60, 100),
            ProgramEvent(0, 0, 1),
            NoteOnEvent(0, 0, 60, 0),
        ], control=PROGRAM_SWITCH)
        self.assertEqual([ev.note for ev in r[2]], [72])

    def test_sustain_follows_scene(self):
        r = run_engine({0: Channel(1), 1: Channel(2)}, [
            CtrlEvent(0, 0, 64, 127),
            ProgramEvent(0, 0, 1),
            CtrlEvent(0, 0, 64, 0),
            CtrlEvent(0, 0, 64, 0),
        ], control=PROGRAM_SWITCH)
        self.assertEqual(r[2], [CtrlEvent(0, 1, 64, 0)])
        self.assertEqual(r[3], [CtrlEvent(0, 2, 64, 0)])

    def test_half_pedal_uses_current_scene(self):
        r = run_engine({0: Channel(1), 1: Channel(2)}, [
            CtrlEvent(0, 0, 64, 127),
            ProgramEvent(0, 0, 1),
            CtrlEvent(0, 0, 64, 64),
        ], control=PROGRAM_SWITCH)
        self.assertEqual(r[2], [CtrlEvent(0, 2, 64, 64)])

    # --- scene switching -------------------------------------------------

    def test_switch_to_missing_scene_is_ignored(self):
        r = run_engine({0: Transpose(1), 1: Transpose(2)}, [
            ProgramEvent(0, 0, 0),
            ProgramEvent(0, 0, 7),
            NoteOnEvent(0, 0, 60, 100),
        ], control=PROGRAM_SWITCH)
        self.assertEqual(r[2], [NoteOnEvent(0, 0, 61, 100)])

    def test_switch_to_missing_scene_runs_no_exit_patch(self):
        r = run_engine({
            0: Scene("a", Pass(), exit_patch=Ctrl(0, 0, 2, 2)),
            1: Pass(),
        }, [
            ProgramEvent(0, 0, 0),
            ProgramEvent(0, 0, 7),
        ], control=PROGRAM_SWITCH)
        self.assertEqual(r[1], [ProgramEvent(0, 0, 7)])

    def test_init_and_exit_patches(self):
        r = run_engine({
            0: Scene("a", Pass(), init_patch=Ctrl(0, 0, 1, 1),
                     exit_patch=Ctrl(0, 0, 2, 2)),
            1: Scene("b", Pass(), init_patch=Ctrl(0, 0, 3, 3),
                     exit_patch=Ctrl(0, 0, 4, 4)),
        }, [
            ProgramEvent(0, 0, 0),
            ProgramEvent(0, 0, 1),
            ProgramEvent(0, 0, 0),
        ], control=PROGRAM_SWITCH)
        self.assertEqual(r[0], [ProgramEvent(0, 0, 0), CtrlEvent(0, 0, 1, 1)])
        # exit of the old scene comes before init of the new one
        self.assertEqual(r[1], [ProgramEvent(0, 0, 1), CtrlEvent(0, 0, 2, 2),
                                CtrlEvent(0, 0, 3, 3)])
        self.assertEqual(r[2], [ProgramEvent(0, 0, 0), CtrlEvent(0, 0, 4, 4),
                                CtrlEvent(0, 0, 1, 1)])

    def test_init_patch_goes_through_post_but_not_pre(self):
        r = run_engine({
            0: Pass(),
            1: Scene("b", Pass(), init_patch=Ctrl(0, 0, 3, 3)),
        }, [
            ProgramEvent(0, 0, 1),
        ], control=PROGRAM_SWITCH, pre=CtrlMap(3, 30), post=CtrlMap(3, 99))
        self.assertIn(CtrlEvent(0, 0, 99, 3), r[0])
        self.assertNotIn(CtrlEvent(0, 0, 30, 3), r[0])

    def test_init_patch_sees_new_scene(self):
        seen = []
        def record(ev):
            seen.append(engine.current_scene())
        run_engine({
            0: Pass(),
            1: Scene("b", Pass(), init_patch=Call(record)),
        }, [ProgramEvent(0, 0, 0), ProgramEvent(0, 0, 1)],
         control=PROGRAM_SWITCH)
        import time
        time.sleep(0.2)
        self.assertEqual(seen, [1])

    def test_scene_switch_hook(self):
        calls = []
        class Hook(object):
            def on_switch_scene(self, scene, subscene):
                calls.append((scene, subscene))
        hook(Hook())
        run_engine({0: Pass(), 1: Pass()}, [
            ProgramEvent(0, 0, 1),
            ProgramEvent(0, 0, 7),      # missing: no hook call
            ProgramEvent(0, 0, 0),
        ], control=PROGRAM_SWITCH)
        self.assertEqual(calls, [(1, 0), (0, 0)])

    def test_subscene_wrap(self):
        g = {0: SceneGroup("g", [Transpose(1), Transpose(2), Transpose(3)])}
        ctl = Fork([PROGRAM_SWITCH,
                    CtrlFilter(1) >> SubSceneSwitch(offset=1),
                    CtrlFilter(2) >> SubSceneSwitch(offset=-1)])
        n = NoteOnEvent(0, 0, 60, 100)
        up, down = CtrlEvent(0, 0, 1, 0), CtrlEvent(0, 0, 2, 0)
        r = run_engine(g, [ProgramEvent(0, 0, 0), n, up, n, up, n, up, n,
                           down, n], control=ctl)
        notes = [x[0].note for x in r if x and x[0].type == NOTEON]
        self.assertEqual(notes, [61, 62, 63, 61, 63])

    def test_subscene_no_wrap(self):
        g = {0: SceneGroup("g", [Transpose(1), Transpose(2)])}
        ctl = Fork([PROGRAM_SWITCH,
                    CtrlFilter(1) >> SubSceneSwitch(offset=1, wrap=False),
                    CtrlFilter(2) >> SubSceneSwitch(offset=-1, wrap=False)])
        n = NoteOnEvent(0, 0, 60, 100)
        up, down = CtrlEvent(0, 0, 1, 0), CtrlEvent(0, 0, 2, 0)
        r = run_engine(g, [ProgramEvent(0, 0, 0), down, n, up, up, up, n],
                       control=ctl)
        notes = [x[0].note for x in r if x and x[0].type == NOTEON]
        self.assertEqual(notes, [61, 62])

    def test_scene_switch_from_patch_takes_effect_after_event(self):
        # the event that triggers the switch is still processed by the old
        # scene; the new one applies from the next event
        r = run_engine({
            0: Fork([KeyFilter(0) >> SceneSwitch(1) >> Discard(),
                     ~KeyFilter(0) >> Transpose(1)]),
            1: Transpose(2),
        }, [
            NoteOnEvent(0, 0, 60, 100),
            NoteOnEvent(0, 0, 0, 100),
            NoteOnEvent(0, 0, 60, 100),
        ])
        self.assertEqual(r[0], [NoteOnEvent(0, 0, 61, 100)])
        self.assertEqual(r[2], [NoteOnEvent(0, 0, 62, 100)])

    # --- control / pre / post ------------------------------------------

    def test_pre_scene_post_order(self):
        r = run_engine({0: Transpose(1)}, [NoteOnEvent(0, 0, 10, 100)],
                       pre=Transpose(10), post=Transpose(100))
        self.assertEqual(r[0], [NoteOnEvent(0, 0, 121, 100)])

    def test_control_patch_output_is_not_routed_through_scene(self):
        r = run_engine({0: Transpose(1)}, [NoteOnEvent(0, 0, 10, 100)],
                       control=Channel(5))
        self.assertEqual(sorted(r[0], key=lambda e: e.channel),
                         [NoteOnEvent(0, 0, 11, 100),
                          NoteOnEvent(0, 5, 10, 100)])

    def test_scene_without_events_still_runs_post(self):
        r = run_engine({0: Discard()}, [NoteOnEvent(0, 0, 10, 100)],
                       post=Transpose(100))
        self.assertEqual(r[0], [])

    @unittest.expectedFailure
    def test_process_event_without_scene_zero(self):
        # process_event() before start() falls back to scene 0.  With no
        # scene 0 (data_offset=0 and scenes numbered from 1), the engine
        # dereferences std::map::end() and segfaults.
        p = run_isolated("""
            e = engine.Engine()
            e.setup({1: Pass(), 2: Pass()}, None, None, None)
            e.process_event(NoteOnEvent(0, 0, 60, 100))
            print('ok')
        """)
        self.assertIsNotNone(p, 'timed out')
        self.assertEqual(p.returncode, 0, p.stderr)


class SanitizeTestCase(MididingsTestCase):
    """
    The engine sanitizes every output event.  These run raw events through
    Process() so that the Python-side argument checks are bypassed.
    """

    def setUp(self):
        MididingsTestCase.setUp(self)
        config(silent=True)

    def out(self, make):
        def f(ev):
            r = MidiEvent(*make)
            return r
        (r,) = run_engine({0: Process(f)}, [NoteOnEvent(0, 0, 60, 100)])
        return [(ev.type, ev.channel_, ev.data1, ev.data2) for ev in r]

    def test_note_range(self):
        self.assertEqual(self.out((NOTEON, 0, 0, 0, 100)),
                         [(NOTEON, 0, 0, 100)])
        self.assertEqual(self.out((NOTEON, 0, 0, 127, 100)),
                         [(NOTEON, 0, 127, 100)])
        self.assertEqual(self.out((NOTEON, 0, 0, 128, 100)), [])
        self.assertEqual(self.out((NOTEOFF, 0, 0, -1, 100)), [])

    def test_velocity_clamped(self):
        self.assertEqual(self.out((NOTEON, 0, 0, 60, 200)),
                         [(NOTEON, 0, 60, 127)])
        self.assertEqual(self.out((NOTEON, 0, 0, 60, -5)),
                         [(NOTEON, 0, 60, 0)])

    def test_channel_range(self):
        self.assertEqual(self.out((CTRL, 0, 15, 1, 1)), [(CTRL, 15, 1, 1)])
        self.assertEqual(self.out((CTRL, 0, 16, 1, 1)), [])
        self.assertEqual(self.out((CTRL, 0, -1, 1, 1)), [])

    def test_negative_port(self):
        self.assertEqual(self.out((CTRL, -1, 0, 1, 1)), [])

    def test_ctrl(self):
        self.assertEqual(self.out((CTRL, 0, 0, 128, 1)), [])
        self.assertEqual(self.out((CTRL, 0, 0, 7, 300)), [(CTRL, 0, 7, 127)])
        self.assertEqual(self.out((CTRL, 0, 0, 7, -3)), [(CTRL, 0, 7, 0)])

    def test_pitchbend_clamped(self):
        self.assertEqual(self.out((PITCHBEND, 0, 0, 0, 9000)),
                         [(PITCHBEND, 0, 0, 8191)])
        self.assertEqual(self.out((PITCHBEND, 0, 0, 0, -9000)),
                         [(PITCHBEND, 0, 0, -8192)])

    def test_aftertouch_clamped(self):
        self.assertEqual(self.out((AFTERTOUCH, 0, 0, 0, 500)),
                         [(AFTERTOUCH, 0, 0, 127)])

    @unittest.expectedFailure
    def test_poly_aftertouch_clamped(self):
        # channel aftertouch is clamped to 0..127 but poly aftertouch passes
        # through unchanged, so out-of-range values reach the MIDI output
        self.assertEqual(self.out((POLY_AFTERTOUCH, 0, 0, 60, 500)),
                         [(POLY_AFTERTOUCH, 0, 60, 127)])

    @unittest.expectedFailure
    def test_poly_aftertouch_note_range(self):
        self.assertEqual(self.out((POLY_AFTERTOUCH, 0, 0, 200, 1)), [])

    def test_program_range(self):
        self.assertEqual(self.out((PROGRAM, 0, 0, 0, 127)),
                         [(PROGRAM, 0, 0, 127)])
        self.assertEqual(self.out((PROGRAM, 0, 0, 0, 128)), [])

    def test_dummy_events_dropped(self):
        self.assertEqual(self.out((DUMMY, 0, 0, 0, 0)), [])

    def test_sysex_framing(self):
        def run(data):
            def f(ev):
                r = MidiEvent(SYSEX, 0, 0, 0, 0)
                r.sysex_ = data
                return r
            (r,) = run_engine({0: Process(f)}, [NoteOnEvent(0, 0, 60, 1)])
            return len(r)
        self.assertEqual(run(bytearray(b'\xf0\xf7')), 1)
        self.assertEqual(run(bytearray(b'\xf0\x01\xf7')), 1)
        self.assertEqual(run(bytearray(b'\xf0\x01')), 0)
        self.assertEqual(run(bytearray(b'\x01\xf7')), 0)
        self.assertEqual(run(bytearray(b'\xf0')), 0)
