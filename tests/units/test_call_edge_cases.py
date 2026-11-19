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
Process() and Call(): what Python functions may return, how errors are
contained, large fan-out, and the asynchronous call queue.
"""

from tests.helpers import *

from mididings import *
from mididings.event import *

import threading
import time


class ProcessEdgeCaseTestCase(MididingsTestCase):

    def setUp(self):
        MididingsTestCase.setUp(self)
        config(silent=True)
        self.ev = NoteOnEvent(0, 0, 60, 100)

    def run1(self, f, events=None):
        return run_engine({0: Process(f)}, events or [self.ev])

    def test_return_none_and_empty(self):
        self.assertEqual(self.run1(lambda ev: None), [[]])
        self.assertEqual(self.run1(lambda ev: []), [[]])

    def test_return_generator(self):
        def gen(ev):
            yield ev
            yield CtrlEvent(0, 0, 1, 2)
        self.assertEqual(self.run1(gen),
                         [[self.ev, CtrlEvent(0, 0, 1, 2)]])

    def test_return_empty_generator(self):
        def gen(ev):
            return
            yield
        self.assertEqual(self.run1(gen), [[]])

    @unittest.expectedFailure
    def test_return_tuple(self):
        # tuples pass the Python-side sequence check, but the C++ side
        # insists on a list, so the event is dropped with a TypeError
        self.assertEqual(self.run1(lambda ev: (ev, ev)), [[self.ev, self.ev]])

    def test_return_same_object_twice(self):
        r = self.run1(lambda ev: [ev, ev])
        self.assertEqual(r, [[self.ev, self.ev]])

    def test_returned_events_are_independent(self):
        # the same Python object returned twice must yield two independent
        # events downstream
        r = run_engine({0: Process(lambda ev: [ev, ev]) >>
                           Fork([KeyFilter(60) >> Transpose(1)])},
                       [self.ev])
        self.assertEqual(r, [[NoteOnEvent(0, 0, 61, 100),
                              NoteOnEvent(0, 0, 61, 100)]])

    def test_input_event_not_modified_for_caller(self):
        # modifying the event inside Process() must not change the event
        # object that was passed to process_event()
        ev = NoteOnEvent(0, 0, 60, 100)
        def f(e):
            e.note = 10
            return e
        run_engine({0: Process(f)}, [ev])
        self.assertEqual(ev.note, 60)

    def test_exception_drops_event_and_engine_continues(self):
        calls = []
        def f(ev):
            calls.append(ev.note)
            if ev.note == 61:
                raise RuntimeError("boom")
            return ev
        events = [NoteOnEvent(0, 0, n, 100) for n in (60, 61, 62)]
        r = run_engine({0: Process(f)}, events)
        self.assertEqual(calls, [60, 61, 62])
        self.assertEqual(r, [[events[0]], [], [events[2]]])

    def test_exception_in_generator_midway(self):
        def gen(ev):
            yield ev
            raise RuntimeError("boom")
        self.assertEqual(self.run1(gen), [[]])

    def test_non_event_return_drops_event(self):
        for value in (5, "x", [self.ev, 5]):
            self.assertEqual(self.run1(lambda ev: value), [[]], repr(value))

    def test_large_fan_out(self):
        # more events than config::MAX_EVENTS (1024) from a single input
        n = 3000
        r = self.run1(lambda ev: [NoteOnEvent(0, 0, i % 128, 100)
                                  for i in range(n)])
        self.assertEqual(len(r[0]), n)
        self.assertEqual([e.note for e in r[0][:130]],
                         [i % 128 for i in range(130)])

    def test_large_fork_fan_out(self):
        p = (Fork([Transpose(i) for i in range(40)]) >>
             Fork([Velocity(offset=-i) for i in range(40)]))
        (r,) = run_engine({0: p}, [self.ev])
        self.assertEqual(len(r), 1600)

    def test_fork_removes_duplicates_by_default(self):
        (r,) = run_engine({0: Fork([Pass(), Pass()])}, [self.ev])
        self.assertEqual(r, [self.ev])
        (r,) = run_engine({0: Fork([Pass(), Pass()],
                                  remove_duplicates=False)}, [self.ev])
        self.assertEqual(r, [self.ev, self.ev])

    def test_nested_process(self):
        p = Process(lambda ev: [ev, CtrlEvent(0, 0, 1, 1)]) >> \
            Process(lambda ev: ev if ev.type == CTRL else None)
        self.assertEqual(run_engine({0: p}, [self.ev]),
                         [[CtrlEvent(0, 0, 1, 1)]])

    def test_process_can_call_engine_functions(self):
        # calling back into the engine from inside Process() must not
        # deadlock (the engine holds its process mutex here)
        seen = []
        def f(ev):
            seen.append((engine.current_scene(), engine.time() >= 0))
            return ev
        run_engine({0: Process(f)}, [self.ev])
        self.assertEqual(len(seen), 1)


class CallEdgeCaseTestCase(MididingsTestCase):

    def setUp(self):
        MididingsTestCase.setUp(self)
        config(silent=True)

    def test_call_does_not_block_and_keeps_order(self):
        seen = []
        def f(ev):
            seen.append(ev.note)
        events = [NoteOnEvent(0, 0, i, 100) for i in range(100)]
        keep = []
        r = run_engine({0: Call(f)}, events, keep=keep)
        self.assertEqual(r, [[]] * 100)
        self.assertTrue(wait_for(lambda: len(seen) == 100))
        self.assertEqual(seen, list(range(100)))

    def test_call_exception_does_not_stop_later_calls(self):
        seen = []
        def f(ev):
            seen.append(ev.note)
            if ev.note == 1:
                raise RuntimeError("boom")
        keep = []
        run_engine({0: Call(f)}, [NoteOnEvent(0, 0, n, 100)
                                  for n in range(3)], keep=keep)
        self.assertTrue(wait_for(lambda: len(seen) == 3))

    def test_call_queue_overflow_does_not_crash(self):
        # the async queue holds config::MAX_ASYNC_CALLS (256) entries;
        # overflowing it must not crash or deadlock.  Events beyond
        # capacity may be dropped, but those that run keep their order.
        p = run_isolated("""
            import time
            seen = []
            def f(ev):
                seen.append(ev.data1 + 128 * ev.data2)
                time.sleep(0.001)
            e = engine.Engine()
            e.setup({0: Call(f)}, None, None, None)
            for i in range(600):
                e.process_event(NoteOnEvent(0, 0, i % 128, i // 128))
            # wait until the queue has drained: no new calls for 1 second
            n = -1
            while n != len(seen):
                n = len(seen)
                time.sleep(1)
            done = list(seen)
            assert done == sorted(done), done
            assert 0 < len(done) <= 600, len(done)
            print('ok')
        """)
        self.assertIsNotNone(p, 'timed out')
        self.assertEqual(p.stdout.strip(), 'ok', p.stderr)

    @unittest.expectedFailure
    def test_call_event_valid_after_return(self):
        # Call() functions receive a pointer into a stack slot of the async
        # thread; an event kept after the function returns is overwritten by
        # later events (or reads freed memory)
        p = run_isolated("""
            import time
            kept = []
            e = engine.Engine()
            e.setup({0: Call(lambda ev: kept.append(ev))}, None, None, None)
            def wait(n):
                end = time.time() + 10
                while len(kept) < n and time.time() < end:
                    time.sleep(0.01)
                assert len(kept) == n, 'Call() never ran'
            e.process_event(NoteOnEvent(0, 0, 60, 100))
            wait(1)
            e.process_event(CtrlEvent(0, 1, 7, 42))
            wait(2)
            assert (kept[0].type_, kept[0].channel_, kept[0].data1,
                    kept[0].data2) == (NOTEON, 0, 60, 100), kept[0].data1
            print('ok')
        """)
        self.assertIsNotNone(p, 'timed out')
        self.assertEqual(p.stdout.strip(), 'ok', p.stderr)

    def test_call_thread_gets_a_copy(self):
        got = []
        done = threading.Event()
        def f(ev):
            time.sleep(0.1)
            got.append((ev.note, ev.velocity))
            done.set()
        keep = []
        run_engine({0: Call(thread=f)}, [NoteOnEvent(0, 0, 60, 100),
                                         NoteOnEvent(0, 0, 61, 101)],
                   keep=keep)
        self.assertTrue(wait_for(lambda: len(got) == 2))
        self.assertEqual(sorted(got), [(60, 100), (61, 101)])
