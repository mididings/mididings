# Changelog

All notable changes to this project will be documented in this file.

## 20250818 - 2026-02-12

### Bug Fixes

- use raw string literal for regex pattern

### Build

- update license metadata
- update minimum supported python version
- remove justfile

### Documentation

- update licensing information
- switch to Furo theme, drop sphinxcontrib.fulltoc extension and remove nasophon theme files
- remove outdated NEWS file
- add git-cliff configuration for changelog generation
- update changelog
- update README with additional badges and section headers
- update Aeolus URL
- remove sphinxcontrib-fulltoc from documentation dependencies
- update changelog
- remove 'justfile' from REUSE.toml annotations
- fix syntax by adding missing comma in extensions list
- Increase the size of the main features
- remove search ref (#33)
- Replace c-domain for py-domain grammar
- increase toc depth to 3 levels
- Add commit parsers to group legacy unconvential commits
- Update build instructions for documentation generation

### Refactor

- update liblo refs again

## 20250818 - 2026-02-12

### Bug Fixes

- gcc warning caused by a previous commit
- update boost header (atomic_count)

### Build

- remove generated man pages when `make clean` is invoked
- add markdown linting to makefile
- switch from make to just
- use python3 instead of plain python
- add script for upgrading version strings project-wide
- standardise 'rm' command
- add dependencies: boost, alsa, jack
- provide extension module name "_mididings"
- install other files
- fix project name vs. library name
- fix installation of python files
- add missing backend source files to build file
- make ALSA and JACK optional dependencies
- set C++ to C++17
- conditionally compile jack, alsa backend compilation units
- generate and install man pages
- set minimum required meson version
- man: fix install directory
- have version string in one place exactly
- generate and install html docs (WIP)
- don't generate docs when building a wheel through PEP517 (e.g., pip)
- use version string from meson.build also in docs
- remove unused setup.py
- add list required packages for a few linux distros
- add missing config file

### CI

- implement automatic build and test
- run on ubuntu 22.04 and 24.04
- run actions on github-ci branch as well as primary
- use matrix.os as key for pkglist directly
- mask ubuntu 22.04 with python 3.11

### Documentation

- add instructions for building from source to README
- throw sphinx configuration through black
- remove makefiles from reuse list
- add build scripts to reuse list
- update README to use Just instead of Make
- change copyright message to include all contributors
- add missing documentation for mididings.{util,engine}
- ensure duplicate names do not appear in ToC
- Update for meson

### Other (unconventional)

- setup meson-python as build system (wip)
- ignore overloaded virtual warnings in specific places
- mask boost-python safety-guard (false positive)
- add patterns for emacs' temporary files
- add missing dependencies

### Refactor

- drop support for scons build system
- move livedings usage of optparse to argparse
- move mididings usage of optparse to argparse
- remove unused variable 'debug' in setup.py
- ensure cppcheck scans header files
- simplify buildpath script
- update link to Arch package
- update version update script for meson
- replace dependency pyliblo with pyliblo3

### Styling

- change various generated strings to f-strings method

### Testing

- ensure versions match project-wide
- update version check for meson
- fix version check for documentation

## 20230114 - 2023-01-14

### Build

- update version

### Documentation

- update README with more links to documentation
- add missing top-level header to README

### Other (unconventional)

- Send an OSC message when the OSC interface starts or stops
- Allow call of the /quit and /restart OSC messages in LiveOSC class
- Update documentation

## 20230111 - 2023-01-11

### Bug Fixes

- blowup in SubSceneSwitch

### Build

- move from distutils to sysconfig
- move from distutils to setuptools
- fine-tune MANIFEST.in
- add reuse/license files to MANIFEST.in
- simplify gitignore
- add Makefile
- set minimum version for build dependencies
- add cache directories to gitignore

### Documentation

- update readme
- add missing link to original documentation
- add information about mailing list
- add short blurb & features to README
- remove vendored sphinx theme - pydoctheme
- rearrange licenses
- initial attempt to comply with reuse specification
- add note about optional dependencies to readme
- update documentation URLs
- resolve deprecation warning for escape sequences
- resolve deprecation warning for escape sequences

### Features

- Add support for get_client_name() and get_client_id() to engine
- Add new example script to show usage of `mididing.process_file`.
- add man pages

### Other (unconventional)

- Put duplicated code into aux function.
- Correct note about pysmf dependency in docstring
- accept strings in ascii hexadecimal notation with no whitespace between bytes

### Refactor

- switch setup.py to f-strings
- move send_midi's usage of optparse to argparse
- introduce pyproject.toml for metadata & optional dependencies
- remove more python 2 specific code
- even more python 2 code removed!
- move function definition out of loop

### Styling

- throw send_midi through black & convert to f-strings

## 20221230 - 2022-12-30

### Bug Fixes

- fixed assert for pitch bend
- fixed setup.py
- fixed Print() portname length when printing just numbers
- fixed patch_switch() off-by-one error
- fixed warnings about unused parameters
- fix VelocityGradient note name handling
- fixed CtrlValueSplit for single controller values
- fixed backend thread termination
- fixed dummy backend / unit test
- fixed smf backend error handling
- fixed util.note_range() for single notes
- fixed and improved aeolus example
- fixed incorrect reference to _time in engine.py
- fixed boost_lib_name() to return default lib name when none is found
- fixed segfault when scene 1 didn't exist; start with the first existing scene instead
- fixed error when initial_scene is None
- fixed KeyFilter() with open note range
- fixed PedalToNoteoff(), broken ages ago by changing CtrlFilter() semantics
- fixed event pickling, moved picking support to python
- fixed PedalToNoteoff() for sostenuto (don't send note-off when releasing pedal while key is still pressed)
- fixed import in livedings/OSCInterface example
- fixed horribly broken CtrlRange()
- fixed compilation issues with some python/boost version due to bad include iorder
- fixed incorrectly name engine functions (removed get_)
- fixed note names for python 3
- fixed operator != for MidiEvent objects
- fixed element deletion while iterating
- fix PitchbendEvent(), thanks to Димон Русский
- fix using EVENT_* constants in Program() generator
- fix accidental build error
- fix python3 build issue in python converters
- fix SysExFilter(manufacturer)
- fix accidental change of octave_offset docs
- fix SysExEvent() for data_offset == 1
- fix NoDataOffset repr/str for python3
- fix unit test
- fix MidiEvent pickling for python 3
- fix cyclic reference in Print()
- fix AftertouchEvent(). just like PitchbendEvent() before, the wrong data field was initialized
- fix stupid test
- fix python2.5 compatibility (collections.Callable does not exist)
- fix copy&paste error
- fix process_file() which has been broken for years. good thing i test this stuff on a regular basis...
- fix PedalToNoteoff() to always send a note-off first when the same already held note is played again
- fix floating split point: never let the two reference points go beyond the margin
- fix Output() parameters pan and expression (were previously sending same value as volume, stupid copy&paste...)
- fix mididings -I and -O parameters for python3 build
- fix exception caused by typo in voices.py
- fix ALSA connection error reporting
- fix dropped events when using output_event()
- fix yet another stupid late night editing mistake
- fix copy&paste variable name error in Call(thread)
- fix error in Call(callable) test case.
- fix build with empty LIBRARY_PATH
- fix error in JACK and ALSA port connections
- fixed Callable issue
- deprecated inspect.getargspec() function
- switch to formatargspec() wrapper
- remove blocking of NOTEON messages with zero velocity

### Build

- build python_module.o with -W -Wall like any other object file
- build/dist stuff
- build constraints once when the function is being decorated, instead of every time the function is called
- build with debug info by default

### Documentation

- documented Call()
- doc update
- documentation fix
- documented new Output() functionality
- documentation update
- document mididings.extra.gm
- Update README
- Update README
- Update README
- Update README
- Update README
- Update README
- Update README
- doc-html/ build from doc/ with sphinx replaces former www-copy
- Update README
- add new fields to setup.py

### Features

- added MANIFEST
- allow ProgramChange/ControlChange with one/two parameters
- allow passing single patch directly to run/Setup
- added Divide()
- added ProgFilter
- added CtrlValueFilter
- added example scripts
- added license and README
- allow multiple arguments for Filter
- added Setup::sanitize_event() and Sanitize unit
- added mididings.util.only
- added init_fold example
- added missing files to manifest
- added 'verbose' parameter
- added start_delay config option
- allow start_delay = 0 to wait for keypress
- added CallAsync() and CallThread()
- added python_caller.*, moved code from Call
- added PrintString()
- added util.py, moved some functions from misc.py
- added remove_duplicates option to config & forks
- added InitAction unit directly to mididings
- allow Patch::process() with constant range
- added mididings.units package to setup.py
- added UnitEx, allow Call() to return multiple events
- added *Event classes
- added config.hh
- added mididings.extra module
- added mididings/extra to manifest
- added jack midi backend (asynchronous event processing outside jack process())
- added jack-rt backend (still needs a lot more testing)
- added comparison operators for curious_alloc
- allow "dummy" backend
- added SendOSC(), SendDBUS() and System()
- added a lot more argument validity checking
- added scripts/mididings
- added basic handling of channel aftertouch
- added first_patch and patch_switch_callback parameters to run_patches()
- added aftertouch support to jack backend
- added CtrlSplit, CtrlValueSplit, ProgSplit
- added CtrlValueSplit with threshold, changed klick example to use it
- added operator // for units
- add bank select support to Output()
- allow patch numbers > 128
- added NEWS
- added NEWS entry for 20081123
- added Output() bank parameter to doc
- added ignore_types parameter to filter, new operator -
- added CallPerChannel()
- added polyphony.py to svn. oops
- added sostenuto parameter to PedalToNoteoff
- added class Scene
- added misc.call_overload() to simplify units with multiple argument specs
- added proper __repr__ for Split
- added hook system, (re)wrote MemorizeScene, OSCInterface and AutoRestart to use it
- add the directory containing the script to sys.path so import works as expected
- added Route() unit
- added event type POLY_AFTERTOUCH (untested)
- added VelocityLimit()
- added manufacturer id parameter to SysExFilter()
- added basic usage info to mididings script
- added link to hooks.py
- added OR selector (operator |)
- added else-rule to splits
- allow half-open note ranges
- added mididings.extra.LatchNotes()
- added extra.Panic()
- added mididings.extra.gm
- added SceneSwitch(offset)
- added support for subscenes
- support wrapping in /mididings/prev_subscene and /mididings/next_subscene
- added package mididings.live to setup.py
- added default arguments to help output
- allow setting initial subscene, save/restore subscene in MemorizeScene()
- support callable objects as parameters to Print(string)
- added support for multiple individual notes to KeyFilter()
- added margin_* parameters to FloatingKeySplit()
- support VelocityLimit() with only one limit
- allow Process() functions to return generators
- added VoiceFilter()
- added OutputTemplate()
- added single-limit versions of VelocityFilter() and CtrlValueFilter()
- added engine.restart() and /mididings/restart OSC message
- added operator +
- added support for python 3.x, fixed support for python 2.5
- support large sysex message (split into multiple chunks) when using the ALSA backend
- added cstdint include back
- added SysEx() example
- added skeleton.py and router.py examples.
- added CtrlCurve() unit
- added engine.time() as a monotonic clock source
- added license section to README
- added sanity checks for config() parameters
- added leading underscore to override and check parameters of setup.config()
- add option -n to livedings, allowing each instance to have its own name
- add Restart() and Quit() in extra.engine
- add missing (??!!) decref
- add MidiEventType <-> int converters
- add unit test for SysExFilter
- add test case for unit execution order
- allow python converters to be compiled with older boost versions which don't support get_pytype()
- add missing _unit_repr to SysEx() unit
- add counted_objects.hh in util
- add test case for Process() using generator
- support docstrings for overload objects
- add unit tests for modifiers
- add @overload.partial, and use it to simplify generator overloads
- add support for exit patches, probably fixing a bug handling non-list init patches along the way
- support "else clause" for selectors using 2-tuple notation. needs more testing
- add docstring for PerChannel
- add build directory and .sconsign.dblite to svn:ignore
- add --enable-c++11 option to setup.py, defaulting to False
- add Transpose(octaves=...)
- add converters to/from bytes, and combine converters for bytes and bytearray in one header
- add finish() method to backend interface, and implement it for JACK realtime backend
- add send_midi() function
- add unfinished version of send_midi script
- add send_midi to the scripts to be installed
- add das::python::scoped_gil_release
- add SND_SEQ_PORT_TYPE_MIDI_GENERIC to alsa ports, thanks to Oleg Samarin.
- add .gitignore
- support constraints for keyword arguments with unspecified names
- allow additional arguments to Process(), Call(), etc.
- add _Unit.add() method, for completeness' sake
- support callable objects in Call() and Process()
- allow types to be used in patches directly
- add documentation of livedings and send_midi
- add varargs automatically instead of using *rest
- add /core to .gitignore
- allow engine with no input or output ports
- add mididings -p option for a simple event logger
- add mididings interactive shell (option -s or -S)
- support user config file
- add mididings.extra.CtrlToSysEx()
- support indented multi-line input
- support reattaching to jack buffered backend
- support SysEx strings in ASCII notation
- allow port/channel of Output() to be omitted
- Add encoding declaration to allow non-ascii chars in metadata
- add some more examples to documentation
- Add Arch Linux PKGBUILD
- implement misc.formatargspec

### Miscellaneous Tasks

- mostly cleanup
- missed one line to clean
- mutex code cleanup in PythonCaller
- some code cleanup
- minor naming cleanup
- some more engine/backend cleanup
- just cleanup
- split PythonCaller::call_now() into smaller functions, cleanup
- some import cleanup
- just cleaning up
- import and formatting cleanup
- better and cleaner from/to-python converters, moved to src/util
- * implement regex-based port connection for alsa and jack backends
- * convert Patch and related methods to template-based code, to allow different underlying container types
- minor cleanup of overload module
- * clean up/fix sysex data conversion
- * clean up event attribute access
- minor cleanup
- * support manipulating sysex data in-place (in python bytearray, not in C++ vector)
- a bit of scene/engine cleanup
- minor useless cleanup
- keep mididings.extra module namespace clean
- generate documentation using sphinx
- reformat code to 80 columns
- command line options for data and octave offset

### Other (unconventional)

- initial import
- put util into namespace das
- first attempt at documentation
- shouldn't have removed this...
- formatting
- hopefully fixed event processing/routing
- preliminary patch switch handling for sustain pedal
- filters now discard other event types
- new test cases
- source tree restructuring:
- print patch switch message only if there are at least two patches
- store only weak reference to Setup, to keep test cases working
- drop events received while waiting for processing to start
- need jack and boost.thread libraries now
- lock mutex only before wait()
- catch exceptions in PythonCaller::call_now()
- major event processing rewrite, retaining the Python-side Chain/Fork structure in C++
- call sanitize again for all outgoing events
- use timed_join() if available (untested)
- yet another change, to compile with boost 1.34.1 again
- split units.py into separate files
- call drop_input() again
- disable garbage collector
- typedef Event* in Engine and PythonCaller
- include mididings.extra in install
- run all init events through post and sanitize patches. d'oh!
- previous commit was bs. fixed return range of Patch::Extended instead.
- hopefully fixed remove_duplicates
- restructured JACK backends
- call Engine::run_async() periodically
- exception message cosmetics
- mention AFTERTOUCH constant in docs
- new SMF backend
- print error messages if pkg-config can't find packages
- output now supports sending volume changes
- new compiler options to reduce binary size
- prettier changelog
- created sysex branch
- preliminary support for scene switching via osc
- the grand renaming: patches are now called scenes, unless they are just patches :)
- derive Chain from list. let's hope this doesn't break anything, needs more testing after a good night's sleep
- marked old functions/units as deprecated using the new 'deprecated' decorator
- find boost libs whether they have the -mt suffix or not
- new class _Selector to allow chaining filters using operator % without parentheses
- new class NamedFlag and NamedBitMask for better repr support
- first attempt at support for system exclusive, system realtime and system common messages
- split units.hh into multiple smaller files
- let AutoRestart() automaticall watch imported local modules
- first version of scripts/mididings
- create a fake entry in sys.modules to make AutoRestart() work
- new ring buffer that can be safely used with C++ objects
- use Call instead of the deprecated CallAsync
- import all units directly from mididings/__init__.py, hopefully fixing the crazy modules-with-the-same-name-mix-up problem
- rewritten unit test
- import all units into mididings.units, for some reason this seems to work now (?!)
- new velocity mode "curve"
- another fix to prevent selecting a nonexisting scene at startup
- note to self: test before commit
- it's 2010, yay
- use misc.overload for SysExFilter
- major documentation update
- new release 20100112
- PROG is PROGRAM again, and all Prog* units were renamed as well
- limit printed sysex data to terminal width
- take length of Print() name into account when printing sysex
- unfinished doc update from two weeks ago
- start event type names with uppercase character
- minor doc fixes
- run jack buffered midi processing at realtime priority
- first commit of livedings
- attempt to fix rare crash when terminating
- first commit of FloatingKeySplit()
- turn off sustain pedal in Panic()
- hopefully fixed crash during termination this time, by adding Backend::stop() method
- when a scene has subscenes, always print the subscene number when switching scenes
- no need for the commas
- include 64 bit library directories in search for boost libs, and use -mt suffix as fallback
- avoid at least some confusion...
- check if backend is null in engine d'tor
- minor doc fixes
- use functools.wraps() to keep names of decorated functions intact
- minor doc improvements
- restructured source by moving backends and units to subdirectories
- nah, too many line breaks
- it's 2011
- * removed pass_others parameter from filter base class, assume true for all filters instead.
- return Fork instead of plain list
- * added apply(), invert() and negate() functions
- completely reorganized and somewhat extended unit tests
- * added event.SysExEvent()
- some improvements to argument checking and error handling in misc and util
- check sysex data in SysExEvent()
- minor documentation changes
- local python3 paths changed
- it's 2012...
- create experimental branch
- some additional documentation, improved formatting, split into smaller files
- * automatically disable alsa backend on non-linux platforms, and change default backend to jack if alsa is not available
- still 20120312...
- some additional type checks
- minor renaming for consistency
- max_size() should apparently return 1, not N
- use custom iterator_range instead of boost's
- save engine args in temporary list for less funny backtraces
- require at least python 2.6
- nah...
- * use python decorator module (new dependency)
- hide basic unit classes behind an underscore, make them available through public functions
- * allow varargs to be used in overloads
- event type and attribute flags now have their own class names
- * NamedBitMask operation return original type for derived classes
- this should have been included in the previous commit
- SysEx() was broken for data_offset == 1 as well
- * more unit tests
- * use counted_objects base class for engine, module, unit and event types
- * pre-allocate plain bytes instead of default constructed T objects. this avoids using placement new on the location of an existing object.
- allocate plain memory for ring buffer instead of objects of type T, and use placement new to construct objects in the buffer
- optionally print a few memory allocation statistics on module unload
- use nested functions instead of member functions. this fixes a memory leak due to cyclic references (_CallBase -> _mididings.Call -> _CallBase.do_call)
- * add mididings.arguments for argument type checking and conversion
- * more unit tests
- * add port/channel default parameter for Generator()
- prefer inspect.formatargspec() and list/dict __repr__() over DIY stuff
- simplify sequenceof()
- minor formatting changes
- * convert constraints from decorated functions to classes
- * add argument checking for config()
- * make unit tests work again, add tests for arguments.py
- minor formatting changes
- include types of arguments used in overload exception message
- * add repr() support to constraints
- * use shorter list constraint syntax
- * preserve sequence types in sequenceof() and tupleof()
- ensure that initial_scene is a tuple, not a list
- * use separate engine wrapper class for virtual function calls
- actually use bitwise or for flags. addition does not necessarily yield the same result!
- * expose midi event types via boost python enum, generate python objects in constants.py automatically
- * add argument checking for functions in event module
- formatting
- much nicer repr() for event types for which utility creation functions exist
- initialize new event from previous one
- verify that events can be reconstructed from their repr() (for every event returned by every patch, and a couple of random events...)
- prevent local variable from leaking into the mididings module
- * add SYSTEM event type definition
- default velocity argument for NoteOff()
- argument checking for Scene and SceneGroup
- again, oops.
- clear globals dict after running script
- * allow None as control/pre/post arguments to run()
- python 3 doesn't have types.NoneType
- * implement python converters from/to shared_ptr<vector>
- adjust backends to use new sysex typedefs
- * add converters to/from python bytes objects
- avoid unnecessary copy of sysex data
- use bytearray instead of bytes (and for python 2.6 or later, not just python 3)
- * remove MidiEvent.param and EVENT_PARAM
- print asterisks instead of argument types in overload error messages. types are confusing because the overloading mechanism doesn't care about types (yet?)
- unit tests for overload module
- finally implement port connections on the python side
- * fix printing of sysex events
- * allow make_event() to create sysex events
- use TransformMode parameters instead of ints
- watch *all* loaded modules for changes. at least until i find a reliable way to tell which modules are "local" and which aren't
- new and hopefully improved logic to figure out which modules to watch for changes
- * add mappingof() constraint
- * add (stricter) typechecking for splits
- bypass the overload mechanism if a dict is passed to run() that is not a valid split
- cache all results of inspect.getargspec() to improve performance
- another tiny performance boost, @accept is now a class
- run unit tests before committing...
- parse portnames when the config changes, not every time engine.in_ports() and engine.out_ports() are called
- retrieve port names directly from setup
- * add -I and -O options to scripts/mididings to specify port connections
- split core.html into core.html and units.html
- preparation for implementing check_sequence() helper function
- use std::atomic_size_t instead of glib functions if c++11 is enabled
- use integer division to ensure that FloatingKeySplit() behaves the same with all python versions
- attempt to reduce stack size of async and jack backend threads if boost 1.50 or later is used
- undo accidental changes
- define program version only at one place in setup.py
- discard sysex data not starting with 0xf0, rather than crashing
- slightly more verbose error messages when regexes don't match any ports
- working implementation of send_midi
- #include <boost/version.hpp> before checking BOOST_VERSION.
- copy boost library name detection from setup.py
- drop support for python 2.5
- drop support for boost versions before 1.37.0
- properly support polyphonic aftertouch
- expose buffer<->MidiEvent conversion to python
- no need for import from __future__
- order events from all JACK input ports by frame
- combine units in a single document
- highlight current document in sidebar
- manually set docstring when using add_varargs
- reformat SConstruct to 80 columns as well
- reduce size of fixed width font a little more
- set __name__ of data_offset_wrapper
- prettier formatting of allocation stats
- rework benchmark code, print results on unload
- relax parameter checking of *Event() functions
- ignore unmatched note off events in VoiceFilter()
- define BOOST_PYTHON_NO_PY_SIGNATURES
- optimize compiler flags, remove default libdirs
- minor formatting and comments
- expose backend creation to Python
- include git revision in version information
- only try to execute valid mididings patches
- clearer error message
- Use boost::unordered_map, fix build issues on OSX
- use offset() instead of NoDataOffset()
- Try to use setuptools, fall back to plain distutils
- Ensure compiler output is in C locale
- convert images to indexed colors
- print actual sysex data value that's out of range
- clarify documentation regarding scene numbers
- validate scene numbers, fix run() argument checking
- include git rev in version number passed to setuptools
- scene -> subscene mispell
- fix template version of destroy()
- fix integer division
- use asyncFlag instead of async
- use inverse logic in connect_matching_ports
- further simplifications
- Add support for jack alias names
- setup for python3-install
- html-doc for mididings from original www-pages
- Explain fix for missing boost_python
- Copied the web site
- Fix boost_python_suffixes to match format of boost_python libraries

### Performance

- perform type checking in operators >>, // and %

### Refactor

- finished renaming midipatch -> mididings
- removed backend.cc
- removed debug parameter from setup/backend
- implemented PythonCall unit
- handle channel/port/program offset in a few more places
- changed python module structure
- updated setup.py
- simplified backend/setup port parameters
- cleanup
- renamed Types.* to TYPE_*
- renamed _MidiEventEx to MidiEvent
- renamed PatchSwitcher -> PatchSwitch
- shortened unit names
- updated "documentation"
- handle multiple sustain pedals
- renamed *.h -> *.hh
- forgot python.cc
- moved benchmark code from backend_alsa to setup
- removed das::exception, use std::runtime_error instead
- updated unit test
- updated documentation
- updated MANIFEST
- moved Call to unit.*
- moved backend/port parameters from run() to config()
- make sure KeySplit and VelocitySplit return Forks, not lists
- make sure init events for the first patch loaded at startup are sent properly
- updated documentation
- don't allow note on with velocity == 0
- make sure init events of the first patch go through postprocessing
- don't call max() on empty sequence
- improved Print() indentation, so everything lines up nicely
- changed structure of backend (now engine calls backend, rather than vice versa)
- more random changes, made too long ago to remember
- updated setup.py (filenames changed)
- make InitAction discard by default
- reverted filter behavior
- updated test cases
- cleanup
- don't use BOOST_FOREACH during processing, seems to have a negative effect on performance
- cleanup/comments
- remove return value from Patch::process() as well
- don't read map elements after erase
- renamed printer.py -> printing.py
- corrected version number in setup.py, release 20080817
- moved to trunk subdirectory
- updated docs/example for Call()
- moved InitAction to units.base, Output to extra.output
- moved Output back to mididings, it's just too useful to be hidden in extra
- cleaned up import statements... i think. favoring explicit relative imports now
- updated documentation
- make use of util.*_number()
- updated docs, added aeolus and klick examples
- removed scripts/mididings again. it's just too damn ugly
- made BackendJack::process() non-pure virtual, to work around errors when it's called before the object is fully constructed
- updated InitAction doc
- leave negative input velocities to VelocityCurve unchanged
- revert previous commit, commited wrong files
- implemented basic handling of channel aftertouch
- eliminated Engine::run(), using boost.lambda instead
- cleanup
- more comments
- move process thread creation to backend
- make SuppressPC return None/ev instead of True/False
- simplified generators
- make InvertedFilter a subclass of Filter
- updated docs
- don't discard aftertouch events in sanitize. d'oh!
- improved klick example description
- updated docs
- changed VelocityFilter so that 0 always means "no limit"
- updated docs
- updated all copyright dates to include 2009
- made ranges half-open
- don't use relative imports
- removed erroneous reference to output_event()
- handle note-on with velocity 0 as note-off (jack/smf backends)
- made Chain a public class, renamed from _Chain
- changed html doc font to sans-serif
- make the portname field in print output at least 2 characters wide
- changed the hack to modifiy compiler flags, so it still works on ubuntu jaunty
- implemented repr() for most units. also, my first metaclass, yay
- removed unit metaclass again, functionality moved to a function decorator
- updated documentation, making sure parameter names match those in the code
- implemented VelocitySlope()
- make use of call_overload() in KeyFilter, VelocityFilter, CtrlValueFilter
- cleanup
- removed VelocityCurve() from docs, minor tweaks for next release
- renamed Call() -> Process() and CallAsync() -> Call()
- made alsa seq backend optional
- moved config and hooks to new module config
- renamed mididings.units.misc to mididings.units.engine to avoid name conflict with mididings.misc
- unified run() and run_scenes()
- unified Print() and PrintString()
- improved documentation and error handling of JACK/ALSA backends
- renamed mididings.config module to mididings.setup to avoid name clash with config() function
- changed semantics of CtrlFilter, CtrlValueFilter, ProgFilter and SysExFilter to block events of other types (again)
- changed selector syntax to use new operator &
- unified Call() and CallThread()
- removed module main, import selected functions directly from setup and engine
- forgot this one
- replaced PORTNAMES_* flags with simple strings
- forgot one again...
- cleanup
- cleanup and comments
- reverted importing osc, dbus and inotify directly into mididings.extra
- simplified overloading mechanism by adding overload decorator, and making name parameter to call_overload optional
- renamed InitAction() to simply Init()
- renamed MidiEvent.type_ to MidiEvent.type
- more doc fixes
- changed call_overload() to query the name of the calling function only when necessary, resulting in a major performance boost
- remove note-on events with velocity < 1
- renamed key -> note in KeyFilter() and KeySplit() to keep names somewhat consistent
- more renaming: ProgChange() -> Prog(), CtrlChange() -> Ctrl()
- removed types parameter from Fork() and Print()
- renamed Note() -> Key()
- more documentation work, removed superfluous examples
- updates NEWS for 20100202
- made bypass feature of Panic() optional
- replaced for-loops with std::find
- made custom theme optional and disabled by default
- replace empty subscene names with (unnamed)
- make OSCInterface accept a single notify port
- don't create scene -1
- cleanup
- reverted rev 312, seems to make things worse by hanging instead of crashing
- updated documentation
- replaced BlackKeys() and WhiteKeys() with KeyColorFilter()
- updated documentation to include new units
- cleaned up KeyFilter() parameters
- simplified FloatingKeySplit(), don't send superfluous note-offs
- make Engine._restart() static so it doesn't keep a reference to the engine
- don't link to libjack when jack midi is disabled
- don't use operator // in FloatingKeySplit() because it fails with two lists
- eliminated the few remaining relative imports
- updated and improved docs
- updated README/NEWS, release 20100318
- removed some problematic sanity checks when creating MidiEvent objects
- updated NEWS for 20100508
- changed MidiEvent() parameters to take data_offset into account
- updated documentation
- updated documentation
- renamed CC# from param to ctrl
- updated setup.py to reflect code restructuring
- make mididings script executable
- moved backend creation from engine to backend/base
- don't use make_shared which isn't available in boost < 1.39.0
- improved VoiceFilter() to work for voices other than highest/lowest
- replaced -p and -l options with positional arguments (options still supported for backward compatibility)
- changed OSCInterface and livedings to use ports 56418 and 56419 by default
- updated docs to reflect param->ctrl renaming
- removed static (which is deprecated in this context) from functions in Mididings namespace
- changed default octave_offset to 1
- removed previously deprecated functions
- don't try to import removed functions run_scenes() and run_patches()
- removed deprecated type_ event attribute
- reverted previous accidental commit
- removed deprecated type_ event attribute
- renamed unit test modules to use test_ as a prefix, this way unittest discover does not require additional parameters
- removed DEBUG_FN calls
- made MidiEvent.sysex a property only in python (preparation for python3 string/bytes fixes)
- changed internal representation of sysex data from string to vector<unsigned char>.
- forgot these in previous commit
- revert changes to octave_offset and filter behavior (r384 and parts of r385), at least for now
- remove ancient sysex branch
- more documentation improvements
- change local python3 lib path
- cleanup
- implement proper from/to-python converters for vector types
- don't use vector_indexing_suite for testing, use converter instead
- move overload mechanism to its own module
- remove accidentally commited line
- more naming cleanup
- replace variable length array (gcc-ism) with alloca() and placement new
- remove unused import
- clean up and document arguments.py
- replace file header
- eliminate global pointer to engine, pass a reference as part of the event buffer instead
- remove unused enum converters
- improved MidiEvent operator equals: only compare the fields which are used by the given event type
- don't reject program number 128 (or 127 without data_offset)
- make sysex events copyable/pickleable
- replace "!= None" with "is not None"
- make TransformMode and EventAttribute enums available to python, generate EVENT_* constants automatically
- more cleanup
- make nullable() a regular constraint
- more python 2.5 fixes, unit tests now work
- forgot to make Split() key nullable
- don't call getargspec() when units are created, but only when their repr() is needed
- make type and value constraints separate classes, avoid expensive calls to isinstance() and inspect.isclass() during argument checking
- rename Engine.process_test() to process_event(), and always include it in mididings builds
- change port connection config data structure to a single variable-length sequence containing both port name and all connections
- change link to decorator module
- updated and improved logic to find out boost library names
- more generic to/from python converters, split into multiple header files
- cleanup and more comments in config.hh, changed int to std::size_t where appropriate
- update copyright date
- change namespace names to all lowercase
- remove unneeded static keyword from config constants
- don't try to start JACK server if it's not already running
- update copyright dates
- move trunk to top level, delete svn branches
- update compiler warning flags
- cleanup
- cleanup
- don't terminate python caller if there's still stuff to do
- remove python 2.5 compatibility cruft
- move buffer<->MidiEvent conversion out of backend class
- remove smf backend, add replacement using pysmf
- update requirements in readme
- don't attempt to set rt priority of less than 1
- revert accidental change to lower case
- move mididings.extra documentation to docstrings
- rename AndSelector and OrSelector to And and Or
- move event attribute descriptions to python source
- change Call() and System() to discard the event
- update docs of Process(), Call() and System()
- improve documentation of mididings.util
- remove blank lines from Velocity() docs
- improve Print() docs
- move general description of splits
- remove examples from "send_midi --help"
- update unit tests now that Call() has changed
- clean up SConstruct
- remove python 2.5 compatibility cruft
- make Fork() and Chain() accept varargs
- don't use code::, add newlines after note::
- don't use boost.lambda; minor cleanup
- update curious_alloc for C++11
- make das::regex default-constructible and copyable
- refactor ALSA port connecting
- implement stop() properly to prevent segfault
- more documentation for mididings command line tool
- rename sysex_to_sequence() to sysex_to_bytearray()
- implement Key() as a single unit in C++
- update .gitignore
- more python3 related updates
- remove PKGBUILD
- remove unnecessary scripts
- remove unnecessary documentation
- fix boost deprecation
- fix PyEval_InitThreads() deprecation
- Moved the assignment of current_patch, current_scene and current_subscene before init patch processing so when calling current_scene() from an init patch it returns the correct scene and not the previous one.
- remove python 2 specific code
- delete documentation build directory

### Styling

- set setup.py permissions to 0644

### Testing

- test cases for event copy and pickle

<!-- generated by git-cliff -->
