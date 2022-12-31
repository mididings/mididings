# mididings

A MIDI router/processor based on Python.

## Installation

### Pip / PyPi

*Note*: Ensure that required dependencies are installed/available before
proceeding.

mididings is available as [`mididings`][pkg-pypi] on PyPi:

```sh
pip install mididings
```

### Arch Linux

For Arch Linux users, mididings is available as [`mididings`][pkg-arch] on the
official repositories:

```sh
pacman -Syu mididings
```

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

Documentation is currently being worked on, the original
[homepage][original-home] & [documentation][original-docs] are valuable resources.

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
[pyliblo]: https://github.com/dsacre/pyliblo
[pysmf]: https://github.com/dsacre/pysmf
[dbus-python]: https://www.freedesktop.org/wiki/Software/dbus/
[pyinotify]: https://github.com/seb-m/pyinotify
[tkinter]: https://docs.python.org/3/library/tkinter.html
[pyxdg]: https://freedesktop.org/wiki/Software/pyxdg/
[spdx-gpl2]: https://spdx.org/licenses/GPL-2.0-or-later.html
[spdx-gfdl]: https://spdx.org/licenses/GFDL-1.3-or-later.html
