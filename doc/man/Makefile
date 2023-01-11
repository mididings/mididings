all: livedings mididings send_midi
	@bash reproducible-man.sh

livedings:
	@scdoc < livedings.scd > livedings.1

mididings:
	@scdoc < mididings.scd > mididings.1

send_midi:
	@scdoc < send_midi.scd > send_midi.1

clean:
	@rm -rf *.1
