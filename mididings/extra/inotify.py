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

import mididings.engine as _engine

import sys as _sys
import os as _os
import time


from watchdog.observers import Observer as _Observer
from watchdog.events import FileSystemEventHandler as _FileSystemEventHandler


class _FileChangeHandler(_FileSystemEventHandler):
    """Internal event handler for file modifications."""

    def __init__(self, on_modified_callback):
        self.on_modified_callback = on_modified_callback

    def on_modified(self, event):
        if not event.is_directory:
            self.on_modified_callback(event.src_path)


class AutoRestart(object):
    """
    Automatically restarts mididings when the script changes.

    This restarts the entire mididings script, so MIDI processing is
    interrupted, and mididings does not take care of reestablishing any
    ALSA/JACK connections that were made manually.
    If the new script contains errors that prevent it from running,
    mididings exits and needs to be restarted manually once the errors
    are fixed.

    :param modules:
        If true, all imported local Python modules are monitored for
        changes as well.

    :param filenames:
        a list of additional files to be monitored.
    """
    def __init__(self, modules=True, filenames=[]):
        self.modules = modules
        self.filenames = filenames
        self.watched_paths = set()
        self.watched_files = set()

    def on_start(self):
        self.observer = _Observer()
        event_handler = _FileChangeHandler(self._process_file_modified)

        if self.modules:
            # find the name of the main script being executed
            if '__mididings_main__' in _sys.modules:
                main_file = _sys.modules['__mididings_main__'].__file__
            elif hasattr(_sys.modules['__main__'], '__file__'):
                main_file = _sys.modules['__main__'].__file__
            else:
                main_file = None

            if main_file:
                base_dir = _os.path.dirname(_os.path.abspath(main_file))

                # add watches for imported modules
                for m in _sys.modules.values():
                    # builtin modules don't have a __file__ attribute
                    if hasattr(m, '__file__'):
                        f = _os.path.abspath(m.__file__)
                        # only watch file if it's in the same directory as the
                        # main script
                        if f.startswith(base_dir):
                            self._add_watch(event_handler, f, base_dir)

        # add watches for additional files
        for f in self.filenames:
            self._add_watch(event_handler, f, base_dir)

        self.observer.start()

    def _add_watch(self, event_handler, filepath, base_dir=None):
        """Add a watch for a file's directory."""
        filepath = _os.path.abspath(filepath)
        dirpath = _os.path.dirname(filepath)
        self.watched_files.add(filepath)
        if dirpath not in self.watched_paths:
            self.observer.schedule(event_handler, dirpath, recursive=False)
            self.watched_paths.add(dirpath)

    def on_exit(self):
        self.observer.stop()
        self.observer.join()

    def _process_file_modified(self, filepath):
        filepath = _os.path.abspath(filepath)

        if filepath not in self.watched_files:
            return

        now = time.monotonic()

        last = getattr(self, "_last_restart_by_file", {}).get(filepath, 0)

        if now - last < 0.3:
            return

        if not hasattr(self, "_last_restart_by_file"):
            self._last_restart_by_file = {}

        self._last_restart_by_file[filepath] = now

        print(f"file '{filepath}' changed, restarting...")
        _engine.restart()
