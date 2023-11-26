configure_file(input: 'mesonconfig.hh.in',
               output: 'mesonconfig.hh',
               configuration: config)

sources = [
  # sources which should always be included
  'engine.cc',
  'patch.cc',
  'python_caller.cc',
  'send_midi.cc',
  'python_module.cc',
  'backend/base.cc',
  'backend/base.cc',
]

# conditionally compiled sources
if config.get('ENABLE_ALSA_SEQ')
  sources += ['backend/alsa.cc']
endif

if config.get('ENABLE_JACK_MIDI')
  sources += [
    'backend/jack.cc',
    'backend/jack_buffered.cc',
    'backend/jack_realtime.cc',
  ]
endif

py.extension_module(
  '_mididings',
  sources,
  dependencies: [boost, alsa, jack],
  install: true)
