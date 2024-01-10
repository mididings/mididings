scdoc = find_program('scdoc', required: false)
if scdoc.found()

  man_pages = {'mididings': '1',
               'livedings': '1',
               'send_midi': '1',
              }

  foreach page, section : man_pages
    name = f'@page@.@section@'
    input = f'@page@.scd'
    custom_target(input,
                  input: files(input),
                  output: name,
                  command: scdoc,
                  feed: true,
                  capture: true,
                  install: true,
                  # Ideally we'd do this:
                  #install_dir: get_option('mandir') / f'man@section@',
                  # But 'mandir' is not a defined installation path for wheel packages.
                  # See: https://docs.python.org/3/library/sysconfig.html#installation-paths
                  # As a workaround we can use 'datadir' as a base and build the rest of the
                  # path manually:
                  install_dir: get_option('datadir') / 'share' / 'man' / f'man@section@',
                 )
  endforeach

else
  warning('The program scdoc could not be found, man pages will not be available.')
endif
