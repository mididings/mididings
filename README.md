[![PyPI](https://img.shields.io/pypi/v/mididings)](https://pypi.org/project/mididings/)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-GPL--2.0--or--later-green)
![Core](https://img.shields.io/badge/core-C%2B%2B-lightgrey)
[![Discourse](https://img.shields.io/badge/community-Discourse-orange)](https://mididings.discourse.group/)

# mididings

A Python-based MIDI router and processor for Linux — expressive, fast,
and built for live performance. Route, filter, transform and split MIDI
events using a clean Python DSL, with all processing handled in C++.

Supports ALSA and JACK MIDI. Available under the GNU GPL.

## Why this fork?

The original mididings by Dominic Sacré has been unmaintained since 2015.
This community fork provides full Python 3 support, a modern build system
(Meson + `pyproject.toml`), updated dependencies, and unified fixes gathered
from various forks. The API remains fully compatible with existing patches
and scripts.

## Features

### MIDI routing and filtering

Filter events by type, channel, note, velocity, and more. Route freely
between any number of input and output ports.

### Modifying and converting MIDI events

Transpose notes, apply velocity curves, remap controller values and ranges,
or convert events to any other MIDI event type. Includes a diatonic
harmonizer, floating split points, latched notes, and more.

### Seamless scene switching

Set up named scenes, each with its own routing and processing, and switch
between them at any time while playing. No dropouts, no stuck notes.

### Monitoring and side effects

Print MIDI events to the console for debugging. Trigger shell commands,
OSC messages, or DBUS calls alongside MIDI output.

## Installation

### PyPI

> **Note:** Ensure system dependencies (ALSA, JACK, Boost) are available
> before installing.

```sh
pip install mididings
```

With optional extras (OSC, MIDI files, DBUS, auto-restart):

```sh
pip install mididings[osc,smf,dbus,autorestart,xdg]
```

Available extras and their dependencies are listed in `pyproject.toml`.

### Arch Linux

```sh
pacman -Syu mididings
```

### From source

The recommended approach for development or testing a new version is a
virtual environment:

```sh
python -m venv venv
source venv/bin/activate
pip install .
```

To verify the installation:

```sh
which mididings
```

To resume work in an existing environment:

```sh
source venv/bin/activate
```

#### System-wide installation

Requires [scdoc][scdoc] and [sphinx][sphinx] if building documentation.

```sh
meson build --prefix=/usr/local
meson compile -C build
meson install -C build
```

#### Packaging options

```sh
# Disable documentation
meson build -Ddocs=disabled -Dman=disabled

# Build documentation separately
meson setup build -Ddocs-only=true
meson compile -C build
cd build && meson install
```

> **Note:** mididings must be installed before building docs with
> `docs-only=true`.

## Dependencies

### Required

- [Python 3][python]
- [ALSA][alsa]
- [JACK][jack]
- [Boost][boost] (Boost.Python, Boost.Thread)
- [glib][glib]
- [decorator][decorator]

### Optional

- [pyliblo3][pyliblo3]: OSC send/receive
- [pysmf][pysmf]: MIDI file read/write via `process_file()`
- [dbus-python][dbus-python]: DBUS messages
- [pyinotify][pyinotify]: auto-restart on script change
- [tkinter][tkinter]: livedings GUI
- [pyxdg][pyxdg]: XDG config file lookup

### Build-time

- [scdoc][scdoc]: man page generation
- [sphinx][sphinx]: HTML documentation (see `pyproject.toml` for modules)

## Documentation and support

- [API documentation][api-docs]
- [GitHub Wiki][gh-wiki]
- [Community forum (Discourse)][discourse]

Additional references:

- [QJackCtl and the Patchbay][qjack]
- [The Python Tutorial][py-tutorial]
- [Guide to the MIDI specification][midi-spec]

## License

mididings is available under the
[GNU General Public License, version 2 or later][spdx-gpl2].

Example scripts in `doc/examples` are available under the
[GNU Free Documentation License 1.3 or later][spdx-gfdl].

[pkg-pypi]: https://pypi.org/project/mididings/
[pkg-arch]: https://archlinux.org/packages/extra/x86_64/mididings/
[python]: https://www.python.org
[alsa]: https://www.alsa-project.org/wiki/Main_Page
[discourse]: https://mididings.discourse.group/
[jack]: https://jackaudio.org
[boost]: https://www.boost.org
[glib]: https://docs.gtk.org/glib/
[decorator]: https://github.com/micheles/decorator
[scdoc]: https://git.sr.ht/~sircmpwn/scdoc
[pyliblo3]: https://github.com/gesellkammer/pyliblo3
[pysmf]: https://github.com/dsacre/pysmf
[dbus-python]: https://www.freedesktop.org/wiki/Software/dbus/
[pyinotify]: https://github.com/seb-m/pyinotify
[tkinter]: https://docs.python.org/3/library/tkinter.html
[pyxdg]: https://freedesktop.org/wiki/Software/pyxdg/
[api-docs]: https://mididings.github.io/mididings/
[gh-wiki]: https://github.com/mididings/mididings/wiki
[qjack]: https://www.rncbc.org/drupal/node/76
[py-tutorial]: https://docs.python.org/3/tutorial/
[midi-spec]: http://www.somascape.org/midi/tech/spec.html
[spdx-gpl2]: https://spdx.org/licenses/GPL-2.0-or-later.html
[spdx-gfdl]: https://spdx.org/licenses/GFDL-1.3-or-later.html
[sphinx]: https://www.sphinx-doc.org/en/master/
