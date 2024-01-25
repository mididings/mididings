sphinx = find_program('sphinx-build')

doc_rst_sources = [
  'main',
  'units',
  'extra-units',
  'connect',
  'start',
  'util',
  'extra',
  'misc',
  'engine',
  'index',
  'event',
  'tools',
]

doc_sources = []
docs = []
foreach rst: doc_rst_sources
  doc_sources += [rst + '.rst']
  docs += [rst + '.html']
endforeach

custom_target('docs',
              command: [sphinx, '-b', 'html', meson.current_source_dir(), meson.current_build_dir() / 'html'],
              input: files(doc_sources),
              output: docs,
              install_dir: get_option('datadir') / 'share/doc/mididings/',
              install: true)
