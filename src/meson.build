py.extension_module(
  # add files here
  '_mididings',
  'engine.cc',
  'patch.cc',
  'python_caller.cc',
  'send_midi.cc',
  'python_module.cc',
  'backend/base.cc',
  'backend/jack_buffered.cc',
  'backend/base.cc',
  'backend/jack.cc',
  'backend/jack_realtime.cc',
  'backend/alsa.cc',
  dependencies: [boost, alsa, jack],
  install: true)
