send_midi(1)

# NAME

send_midi - Send one or more MIDI events via ALSA or JACK

# DESCRIPTION

A simple utility to send MIDI events to any ALSA or JACK MIDI client, using a
terse command line format.

# OPTIONS

*-A*, *--alsa*
	Use the ALSA backend (default).

*-J*, *--jack*
	Use the JACK backend.

*-0*, *--zero-based*
	Determines whether channel & program numbers used in events have a data offset
	applied. When the flag is enabled, the numbers are 0-127. The default range is
	set to 1-128.

*-h*, *--help*
	Shows a brief summary of how to use this program.

*--version*
	Shows the program version.

# EXAMPLES

Send two events to LinuxSampler:0 while using the JACK backend.

	send_midi -J LinuxSampler:0 NOTEON,1,60,127 CTRL,2,7,66

Send a SYSEX command to 14:0.

	send_midi 14:0 SYSEX,F0,23,42,F7

# SEE ALSO

See the online documentation at https://mididings.github.io/mididings/ for
current information on mididings and its related tools.

# BUGS

Bugs? You must be kidding; there are no bugs in this software. But if we happen
to be wrong, submit a bug report with as much detail as possible at
https://github.com/mididings/mididings/issues.

