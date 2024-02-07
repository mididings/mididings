sphinx = find_program('sphinx-build', required: false)

if get_option('docs').enabled() and sphinx.found()

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
foreach rst: doc_rst_sources
  doc_sources += [rst + '.rst']
endforeach

if get_option('docs-only')
  sphinx_deps = []
else
  sphinx_deps = [mididings_extension_module]
endif

custom_target('docs',
              command: [sphinx, '-q', '-b', 'html', meson.current_source_dir(), meson.current_build_dir() / 'html'],
              input: files(doc_sources),
              depends: sphinx_deps,
              output: 'html',
              install_dir: get_option('datadir') / 'doc/mididings',
              install: true,
             )

elif get_option('docs').enabled()
  warning('The program sphinx-build could not be found, html docs will not be available.')
endif
