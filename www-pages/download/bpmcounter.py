#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bpmcounter
#
# Copyright (C) 2005  Dominic Sacré  <dominic.sacre@gmx.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.


import pygtk
pygtk.require('2.0')
import gtk

import time


class MarkupButton(gtk.Button):
    def __init__(self, markup):
        gtk.Button.__init__(self)
        l = gtk.Label()
        l.set_markup_with_mnemonic(markup)
        self.add(l)


class BPMCounter:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_border_width(8)
        self.window.set_resizable(False)
        self.window.connect("destroy", self.destroy)

        vbox = gtk.VBox(False, 8)
        self.window.add(vbox)

        self.label = gtk.Label()
        self.label.set_alignment(0, 0)
        vbox.pack_start(self.label, True, True, 0)

        self.btntap = MarkupButton("<b>_Tap</b>")
        vbox.pack_start(self.btntap, True, True, 0)
        self.btntap.connect("clicked", self.callback_tap)

        hbox = gtk.HBox(False, 8)
        vbox.pack_start(hbox, False, False, 0)

        self.btnreset = gtk.Button("_Reset")
        self.btnreset.set_property("can-focus", False)
        hbox.pack_start(self.btnreset, True, True, 0)
        self.btnreset.connect("clicked", self.callback_reset)

        self.btnquit = gtk.Button("_Quit")
        self.btnquit.set_property("can-focus", False)
        hbox.pack_start(self.btnquit, False, False, 0)
        self.btnquit.connect("clicked", self.destroy)

        self.start = 0.0
        self.beats = 0

        self.update()
        self.window.show_all()

    def callback_tap(self, widget):
        self.beats += 1
        if self.start == 0.0:
            self.start = time.time()
        self.update()

    def callback_reset(self, widget):
        self.start = 0.0
        self.beats = 0
        self.update()

    def update(self):
        bpm = 0
        current = time.time()
        if self.beats > 1:
            bpm = ((self.beats-1) * 60) / (current - self.start)
        self.label.set_markup("<big>BPM: %.2f\nBeats: %d</big>" % (bpm, self.beats))

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()


if __name__ == "__main__":
    BPMCounter().main()
