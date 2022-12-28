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

import inspect
import functools
import itertools
import termios
import fcntl
import struct
import sys

import decorator


def flatten(arg):
    """
    Flatten nested sequences into a single list.
    """
    if issequence(arg):
        return list(itertools.chain(*(flatten(i) for i in arg)))
    else:
        return [arg]


def issequence(seq, accept_string=False):
    """
    Return whether seq is of a sequence type. By default, strings are not
    considered sequences.
    """
    if not accept_string and isinstance(seq, str):
        return False

    try:
        iter(seq)
        return True
    except TypeError:
        return False


def issequenceof(seq, t):
    """
    Return whether seq is a sequence with elements of type t.
    """
    return issequence(seq) and all(isinstance(v, t) for v in seq)


def islambda(f):
    lam = lambda: None
    return isinstance(f, type(lam)) and f.__name__ == lam.__name__


_argspec_cache = {}

def getargspec(f):
    """
    Wrapper around inspect.getargspec() that returns sensible results for
    functools.partial objects.
    All results are cached since inspect.getargspec() is a little slow.
    """
    if f in _argspec_cache:
        return _argspec_cache[f]
    else:
        if isinstance(f, functools.partial):
            argspec = list(inspect.getfullargspec(f.func))
            argspec[0] = argspec[0][len(f.args):]
            r = tuple(argspec)
        else:
            r = inspect.getfullargspec(f)
        _argspec_cache[f] = r
        return r

"""
The inspect.formatargspec() function was dropped in Python 3.11 but we need
it when constructing signature changing decorators based on result of
inspect.getargspec() or inspect.getfullargspec(). The code here implements
inspect.formatargspec() based on Parameter and Signature from inspect module,
which were added in Python 3.6. Thanks to Cyril Jouve for the implementation.
"""
def formatargspec(args, varargs=None, varkw=None, defaults=None,
                  kwonlyargs=(), kwonlydefaults={}, annotations={}):
    if kwonlydefaults is None:
        kwonlydefaults = {}
    ndefaults = len(defaults) if defaults else 0
    parameters = [
        inspect.Parameter(
            arg,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=defaults[i] if i >= 0 else inspect.Parameter.empty,
            annotation=annotations.get(arg, inspect.Parameter.empty),
        ) for i, arg in enumerate(args, ndefaults - len(args))
    ]
    if varargs:
        parameters.append(inspect.Parameter(varargs, inspect.Parameter.VAR_POSITIONAL))
    parameters.extend(
        inspect.Parameter(
            kwonlyarg,
            inspect.Parameter.KEYWORD_ONLY,
            default=kwonlydefaults.get(kwonlyarg, inspect.Parameter.empty),
            annotation=annotations.get(kwonlyarg, inspect.Parameter.empty),
        ) for kwonlyarg in kwonlyargs
    )
    if varkw:
        parameters.append(inspect.Parameter(varkw, inspect.Parameter.VAR_KEYWORD))
    return_annotation = annotations.get('return', inspect.Signature.empty)
    return str(inspect.Signature(parameters, return_annotation=return_annotation))

class deprecated(object):
    def __init__(self, replacement=None):
        self.replacement = None

    def wrapper(self, f, *args, **kwargs):
        # XXX: avoid circular import
        from mididings.setup import get_config

        if (not (hasattr(f, '_already_used') and f._already_used) and
                not get_config('silent')):
            if self.replacement:
                print("%s() is deprecated, please use %s() instead" %
                        (f.__name__, self.replacement))
            else:
                print("%s() is deprecated" % f.__name__)
            f._already_used = True
        return f(*args, **kwargs)

    def __call__(self, f):
        f._deprecated = True
        return decorator.decorator(self.wrapper, f)


class NamedFlag(int):
    """
    An integer type where each value has a name attached to it.
    """
    def __new__(cls, value, name):
        return int.__new__(cls, value)
    def __init__(self, value, name):
        self.name = name
    def __getnewargs__(self):
        return (int(self), self.name)
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name


class NamedBitMask(NamedFlag):
    """
    Like NamedFlag, but bit operations | and ~ are also reflected in the
    resulting value's string representation.
    """
    def __or__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        return type(self)(
            int(self) | int(other),
            '%s|%s' % (self.name, other.name)
        )
    def __invert__(self):
        return type(self)(
            ~int(self) & ((1 << 30) - 1),
            ('~%s' if '|' not in self.name else '~(%s)') % self.name
        )


def prune_globals(g):
    return [n for (n, m) in g.items()
        if not inspect.ismodule(m)
        and not n.startswith('_')
        #and not (hasattr(m, '_deprecated'))
    ]


def sequence_to_hex(data):
    return ' '.join(hex(x)[2:].zfill(2) for x in data)


class bytestring(object):
    def __init__(self, data):
        self.data = data
    def __repr__(self):
        return '\'%s\'' % ''.join('\\x' + hex(x)[2:].zfill(2)
                                    for x in self.data)


def get_terminal_size():
    """
    Return the height and width of the terminal.
    """
    try:
        s = struct.pack("HHHH", 0, 0, 0, 0)
        fd = sys.stdout.fileno()
        x = fcntl.ioctl(fd, termios.TIOCGWINSZ, s)
        t = struct.unpack("HHHH", x)
        return t[0], t[1]
    except Exception:
        return 25, 80
