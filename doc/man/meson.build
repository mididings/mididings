scdoc = find_program('scdoc', required: false)
if get_option('man').enabled() and scdoc.found()

  man_pages = {
    'mididings': '1',
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
                  install_dir: get_option('mandir') / f'man@section@',
                 )
  endforeach

elif get_option('man').enabled()
  warning('The program scdoc could not be found, man pages will not be available.')
endif
