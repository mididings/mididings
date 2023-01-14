# mididings

A MIDI router/processor based on Python, supporting ALSA and JACK MIDI.
It is available under the GNU GPL and currently runs on Linux.

## Features

* MIDI routing and filtering

Filter events depending on their event type, channel, note number, velocity,
etc., and freely route them between an arbitrary number of input and output
ports.

* Modifying and converting MIDI events

Transpose notes, apply velocity curves, change controller values and ranges,
or convert events to any other MIDI event type. mididings also includes more
complex functions like a diatonic harmonizer, floating split points, latched
notes, and more.

* Seamless switching between patches

Set up different "scenes", each with its own MIDI routing and processing,
and switch between them at any time, even while playing. Switching scenes
does not affect notes already held, and does not result in dropouts or stuck
notes!

* MIDI event monitoring, running external commands

Print MIDI event data to the console to help debugging your patches and
configuring your MIDI controllers. In addition to its MIDI output, mididings
can also execute shell commands and send OSC or DBUS messages.

## Installation

### Pip / PyPi

*Note*: Ensure that required dependencies are installed/available before
proceeding.

mididings is available as [`mididings`][pkg-pypi] on PyPi:

```sh
pip install mididings
```

Optional dependencies can be installed, see next section
(Dependencies/Optional)for a list of optional dependencies.

```sh
pip install mididings[osc,smf,dbus,autorestart,xdg]
```

### Arch Linux

For Arch Linux users, mididings is available as [`mididings`][pkg-arch] on the
official repositories:

```sh
pacman -Syu mididings
```

### Source

An additonal dependency is required ([scdoc][scdoc]) and can be uninstalled
afterwards.

```sh
make manpages
python -m build
```

Distribution artifacts (wheel & sdist) can be found in `dist/` folder.

## Dependencies

### Required

* [Python 3][python]
* [ALSA][alsa]
* [JACK][jack]
* [Boost][boost] (Boost.Python, Boost.Thread)
* [glib][glib]
* [decorator][decorator]

### Optional

* [pyliblo][pyliblo]: to send or receieve OSC messages
* [pysmf][pysmf]: to read/write standard MIDI files using the `process_file()` function
* [dbus-python][dbus-python]: to send DBUS messages
* [pyinotify][pyinotify]: to automatically restart when a script changes
* [tkinter][tkinter]: for the livedings GUI
* [pyxdg][pyxdg]: so mididings knows where to look for configuration files

## Documentation

* [API documentation][api-docs]
* [GitHub Wiki][gh-wiki]

Some links that might also be of interest:

* [Original homepage][original-home]
* [Original documentation][original-docs]
* [QJackCtl and the Patchbay][qjack]
* [The Python Tutorial][py-tutorial]
* [Guide to the MIDI specification][midi-spec]

## Support

There is a [mailing list][mailing-list] at Google Groups for any discussion
concerning mididings, including help requests and bug reports.

To post to the list, send mail to <mididings@googlegroups.com>.

## License

mididings is available under the terms of the
[GNU General Public License, version 2 or later][spdx-gpl2].

The example scripts in `doc/examples` are available under the terms of the
[GNU Free Documentation License 1.3 or later][spdx-gfdl].

[pkg-pypi]: https://pypi.org/project/mididings/
[pkg-arch]: https://archlinux.org/packages/community/x86_64/mididings/
[original-home]: https://das.nasophon.de/mididings/
[original-docs]: https://dsacre.github.io/mididings/doc/
[python]: https://www.python.org
[alsa]: https://www.alsa-project.org/wiki/Main_Page
[jack]: https://jackaudio.org
[boost]: https://www.boost.org
[glib]: https://docs.gtk.org/glib/
[decorator]: https://github.com/micheles/decorator
[scdoc]: https://git.sr.ht/~sircmpwn/scdoc
[pyliblo]: https://github.com/dsacre/pyliblo
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
[mailing-list]: https://groups.google.com/g/mididings
[spdx-gpl2]: https://spdx.org/licenses/GPL-2.0-or-later.html
[spdx-gfdl]: https://spdx.org/licenses/GFDL-1.3-or-later.html
