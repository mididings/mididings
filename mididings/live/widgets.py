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

import sys
import tkinter


class AutoScrollbar(tkinter.Scrollbar):
    def set_show_hide(self, show, hide):
        self._show = show
        self._hide = hide

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self._hide()
        else:
            self._show()
        tkinter.Scrollbar.set(self, lo, hi)


class LiveThemedFactory(object):
    def __init__(self, color, color_highlight, color_background):
        self.color = color
        self.color_highlight = color_highlight
        self.color_background = color_background

    def Tk(self, **options):
        w = tkinter.Tk()
        w.config(background=self.color_background)
        w.config(**options)
        return w

    def Frame(self, master, **options):
        w = tkinter.Frame(master)
        w.config(background=self.color)
        w.config(**options)
        return w

    def AutoScrollbar(self, master, **options):
        w = AutoScrollbar(master)
        w.config(
            background=self.color,
            activebackground=self.color_highlight,
            troughcolor=self.color_background,
            borderwidth=1,
            relief='flat',
            width=16,
        )
        w.config(**options)
        return w

    def Listbox(self, master, **options):
        w = tkinter.Listbox(master)
        w.config(
            background=self.color_background,
            foreground=self.color,
            selectbackground=self.color_background,
            selectforeground=self.color_highlight,
            selectborderwidth=0,
            borderwidth=0,
        )
        w.config(**options)
        return w

    def Button(self, master, **options):
        w = tkinter.Button(master)
        w.config(
            background=self.color_background,
            foreground=self.color,
            activebackground=self.color_background,
            activeforeground=self.color_highlight,
            borderwidth=0,
            highlightthickness=0,
            relief='flat',
        )
        w.config(**options)
        return w

    def Canvas(self, master, **options):
        w = tkinter.Canvas(master)
        w.config(background=self.color_background)
        w.config(**options)
        return w

class UnthemedFactory(object):
    def Tk(self, **options):
        w = tkinter.Tk()
        w.config(**options)
        return w

    def Frame(self, master, **options):
        return tkinter.Frame(master, **options)

    def AutoScrollbar(self, master, **options):
        return AutoScrollbar(master, **options)

    def Listbox(self, master, **options):
        return tkinter.Listbox(master, **options)

    def Button(self, master, **options):
        return tkinter.Button(master, **options)

    def Canvas(self, master, **options):
        return tkinter.Canvas(master, **options)
