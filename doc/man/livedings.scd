livedings(1)

# NAME

livedings - A graphical frontend for mididings

# DESCRIPTION

livedings is a graphical front end that allows you to monitor and trigger scene
changes. It runs as a separate application that uses OSC to communicate with
mididings.

By default, livedings uses the standard Tk theme. Specify the -T option to
switch to a custom theme with higher contrast and larger fonts. See
livedings --help for more options.

The buttons at the bottom of the screen can be used to switch to the
previous/next scene, previous/next subscene, and to send all-notes-off messages
(panic) on all output ports. It’s also possible to use the arrow keys to switch
scenes (up/down) and subscenes (left/right).

# OPTIONS

*-h*, *--help*
	show this help message and exit

*-p* _port_
	OSC port mididings is listening on (56418)

*-l* _port_
	OSC port for notifications from mididings (56419)

*-T*
	enable custom theme and larger fonts

*-x* _width_
	width of window in pixels (640)

*-y* _height_
	height of window in pixels (400)

*-w* _width_
	width of scene list in pixels (240)

*-F* _font_
	display font (Sans 14 bold)

*-f* _font_
	scene list font (Sans 10)

*-c* _color_
	text color (gray50)

*-C* _color_
	highlight text color (black)

*-b* _color_
	background color

*-n* _name_
	name to be shown in window title

# SEE ALSO

See the online documentation at https://mididings.github.io/mididings/ for
current information on mididings and its related tools.

# BUGS

Bugs? You must be kidding; there are no bugs in this software. But if we happen
to be wrong, submit a bug report with as much detail as possible at
https://github.com/mididings/mididings/issues.

