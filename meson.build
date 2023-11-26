project('mididings', 'cpp', default_options: ['cpp_std=c++17'])
add_project_arguments('-DUSE_MESON', language: 'cpp')

boost = dependency('boost', modules: ['python3', 'thread'])

# Handle optional dependencies
config = configuration_data()
alsa = dependency('alsa', required: false)
config.set('ENABLE_ALSA_SEQ', alsa.found())

jack = dependency('jack', required: false)
config.set('ENABLE_JACK_MIDI', jack.found())

# Recurse into compilation targets
py = import('python').find_installation(pure: false)
subdir('src')

# Plain copy targets
subdir('mididings')
subdir('scripts')
# subdir('doc/man')
