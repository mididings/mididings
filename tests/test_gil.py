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
Engine.process_event() and Engine.output_event() lock the engine's process
mutex.  The engine holds that mutex while it runs Process() units, which
need the GIL, so a thread that waits for the mutex while holding the GIL
deadlocks against them.

A deadlock leaves the GIL held and freezes the whole interpreter, so each
case runs in a subprocess.  faulthandler ends a hung one after a few
seconds and prints the stacks of all threads.

In each case one thread stands in for the engine thread: it runs a
Process() unit that releases the GIL (time.sleep() here; any I/O or a
long enough computation does the same), and the other thread calls into
the engine meanwhile.
"""

import os
import subprocess
import sys
import textwrap
import unittest

import _mididings

TIMEOUT = 5

PREAMBLE = """
import faulthandler
import threading
import time

faulthandler.dump_traceback_later({timeout}, exit=True)

from mididings import Fork, Process, setup, engine
from mididings.event import CtrlEvent
from mididings.extra import Panic

def slow(ev):
    time.sleep(0.1)
    return ev

def make_engine(backend, patch):
    setup._config_impl(backend=backend, client_name='mididings_test_gil')
    e = engine.Engine()
    e.setup({{setup.get_config('data_offset'): patch}}, None, None, None)
    return e

ev = CtrlEvent(setup.get_config('data_offset'),
               setup.get_config('data_offset'), 7, 64)
"""

# A second thread calls process_event() while the first is inside slow().
PROCESS_EVENT = """
e = make_engine('dummy', Process(slow))
a = threading.Thread(target=e.process_event, args=(ev,))
a.start()
time.sleep(0.05)
e.process_event(ev)
a.join()
print('ok')
"""

# A second thread calls output_event() while the first is inside slow().
OUTPUT_EVENT = """
e = make_engine('alsa', Process(slow))
a = threading.Thread(target=e.process_event, args=(ev,))
a.start()
time.sleep(0.05)
e.output_event(ev)
a.join()
print('ok')
"""

# No thread of our own: Panic() calls output_event() from mididings' own
# thread for Call() units, while the Process() unit next to it runs.
PANIC = """
e = make_engine('alsa', Fork([Panic(), Process(slow)]))
e.process_event(ev)
time.sleep(0.2)     # let the Panic() call finish
print('ok')
"""


def have_alsa():
    return ('alsa' in _mididings.available_backends()
            and os.access('/dev/snd/seq', os.R_OK | os.W_OK))


class GilTestCase(unittest.TestCase):

    def run_case(self, body):
        code = textwrap.dedent(PREAMBLE.format(timeout=TIMEOUT)) + body
        try:
            p = subprocess.run([sys.executable, '-c', code],
                               capture_output=True, text=True,
                               timeout=TIMEOUT + 10)
        except subprocess.TimeoutExpired:
            self.fail('deadlock (subprocess killed)')
        self.assertEqual(p.stdout.strip(), 'ok',
                         'deadlock or error; stderr:\n' + p.stderr)

    def test_process_event_from_thread(self):
        self.run_case(PROCESS_EVENT)

    @unittest.skipUnless(have_alsa(), 'needs the ALSA sequencer')
    def test_output_event_from_thread(self):
        self.run_case(OUTPUT_EVENT)

    @unittest.skipUnless(have_alsa(), 'needs the ALSA sequencer')
    def test_panic_beside_process(self):
        self.run_case(PANIC)
