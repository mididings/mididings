mididings(1)

# NAME

mididings - A MIDI router and processor based on Python.

# DESCRIPTION

The mididings command line tool offers several ways to run patches without
writing full-fledged Python scripts.

# OPTIONS

*--version*
	Display version number of Python & mididings.

*-h*, *--help*
	Display help message.

## BACKEND OPTIONS

*-A*
	Use ALSA sequencer.

*-J*
	Use JACK MIDI (buffered).

*-R*
	Use JACK MIDI (realtime).

*-c* _client name_
	ALSA or JACK client name.

*-i* _ports_
	Number of input ports.

*-o* _ports_
	Number of output ports.

*-I* _connections_
	Input port connections. Regular expression.

*-O* _connections_
	Output port connections. Regular expression.

## GENERAL OPTIONS

*-d* _delay_
	Delay (in seconds) before processing starts.

*-t* _offset_
	Octave offset.

*-z* _offset_
	Offset for port, channel & program numbers.

## MODE OPTIONS

*-f* _filename_
	File name of script to run.

*-s*
	Interactive shell.

*-S*
	Interactive shell with automatic patch execution.

*-p*
	Print MIDI events. No processing is done.

# SEE ALSO

See the online documentation at https://mididings.github.io/mididings/ for
current information on mididings and its related tools.

# BUGS

Bugs? You must be kidding; there are no bugs in this software. But if we happen
to be wrong, submit a bug report with as much detail as possible at
https://github.com/mididings/mididings/issues.

