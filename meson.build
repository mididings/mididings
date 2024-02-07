project('mididings', 'cpp', default_options: ['cpp_std=c++17'], meson_version: '>=0.64.0', version: '20230114')
add_project_arguments('-DUSE_MESON', language: 'cpp')

# Handle optional dependencies
config = configuration_data()
config.set('VERSION', meson.project_version())

alsa = dependency('alsa', required: false)
config.set('ENABLE_ALSA_SEQ', alsa.found())

jack = dependency('jack', required: false)
config.set('ENABLE_JACK_MIDI', jack.found())

if not get_option('docs-only')
  boost = dependency('boost', modules: ['python3', 'thread'])
  py = import('python').find_installation('python3', pure: false)

  # Recurse into compilation targets
  subdir('src')

  # Plain copy targets
  subdir('mididings')
  subdir('scripts')
endif

subdir('doc/man')
subdir('doc')
