# Changelog

All notable changes to this project will be documented in this file.

## 20250818 - 2026-01-27

### Build

- build: update license metadata
- build: update minimum supported python version
- build: remove justfile

### Documentation

- docs: update licensing information
- docs: switch to Furo theme, drop sphinxcontrib.fulltoc extension and remove nasophon theme files
- docs: remove outdated NEWS file
- docs: add git-cliff configuration for changelog generation
- docs: update changelog
- docs: update README with additional badges and section headers
- docs: update Aeolus URL
- docs: remove sphinxcontrib-fulltoc from documentation dependencies

### Refactor

- refactor: update liblo refs again

## 20250818 - 2026-01-27

### Bug Fixes

- fix: gcc warning caused by a previous commit
- fix: update boost header (atomic_count)

### Build

- build: remove generated man pages when `make clean` is invoked
- build: add markdown linting to makefile
- build: switch from make to just
- build: use python3 instead of plain python
- build: add script for upgrading version strings project-wide
- build: standardise 'rm' command
- meson: add dependencies: boost, alsa, jack
- meson: provide extension module name "_mididings"
- meson: install other files
- meson: fix project name vs. library name
- meson: fix installation of python files
- meson: add missing backend source files to build file
- meson: make ALSA and JACK optional dependencies
- meson: set C++ to C++17
- meson: conditionally compile jack, alsa backend compilation units
- meson: generate and install man pages
- meson: set minimum required meson version
- meson: man: fix install directory
- meson: have version string in one place exactly
- meson: generate and install html docs (WIP)
- meson: don't generate docs when building a wheel through PEP517 (e.g., pip)
- meson: use version string from meson.build also in docs
- build: remove unused setup.py
- build: add list required packages for a few linux distros
- build/doc: add missing config file

### CI

- github-ci: implement automatic build and test
- github-ci: run on ubuntu 22.04 and 24.04
- github-ci: run actions on github-ci branch as well as primary
- github-ci: use matrix.os as key for pkglist directly
- github-ci: mask ubuntu 22.04 with python 3.11

### Documentation

- docs: add instructions for building from source to README
- docs: throw sphinx configuration through black
- docs: remove makefiles from reuse list
- docs: add build scripts to reuse list
- docs: update README to use Just instead of Make
- docs: change copyright message to include all contributors
- docs: add missing documentation for mididings.{util,engine}
- docs: ensure duplicate names do not appear in ToC

### Other (unconventional)

- update link to Arch package
- Merge pull request #15 from carpii/primary
- setup meson-python as build system (wip)
- ignore overloaded virtual warnings in specific places
- update version update script for meson
- README: Update for meson
- Merge pull request #16 from romsom/meson
- event: mask boost-python safety-guard (false positive)
- Merge pull request #17 from romsom/mask-boost-python-warning
- gitignore: add patterns for emacs' temporary files
- Merge pull request #19 from romsom/gitignore-emacs-temporary
- pkglist.toml: add missing dependencies
- Merge pull request #18 from romsom/github-ci
- 20250818

### Refactor

- refactor: drop support for scons build system
- refactor: move livedings usage of optparse to argparse
- refactor: move mididings usage of optparse to argparse
- refactor: remove unused variable 'debug' in setup.py
- refactor: ensure cppcheck scans header files
- refactor: simplify buildpath script
- refactor: replace dependency pyliblo with pyliblo3

### Styling

- style: change various generated strings to f-strings method

### Testing

- test: ensure versions match project-wide
- tests: update version check for meson
- tests: fix version check for documentation

## 20230114 - 2023-01-14

### Build

- build: update version

### Documentation

- docs: update README with more links to documentation
- docs: add missing top-level header to README

### Other (unconventional)

- Send an OSC message when the OSC interface starts or stops
- Merge pull request #6 from stefets/osc-issue-5
- Allow call of the /quit and /restart OSC messages in LiveOSC class
- Update documentation
- Merge pull request #8 from stefets/osc-issue-7

## 20230111 - 2023-01-11

### Bug Fixes

- fix: blowup in SubSceneSwitch

### Build

- build: move from distutils to sysconfig
- build: move from distutils to setuptools
- build: fine-tune MANIFEST.in
- build: add reuse/license files to MANIFEST.in
- build: simplify gitignore
- build: add Makefile
- build: set minimum version for build dependencies
- build: add cache directories to gitignore

### Documentation

- docs: update readme
- docs: add missing link to original documentation
- docs: add information about mailing list
- docs: add short blurb & features to README
- docs: remove vendored sphinx theme - pydoctheme
- docs: rearrange licenses
- docs: initial attempt to comply with reuse specification
- docs: add note about optional dependencies to readme
- docs: update documentation URLs
- docs: resolve deprecation warning for escape sequences
- docs: resolve deprecation warning for escape sequences

### Features

- feat: add man pages

### Other (unconventional)

- Put duplicated code into aux function.
- Add support for get_client_name() and get_client_id() to engine
- Add new example script to show usage of `mididing.process_file`.
- Correct note about pysmf dependency in docstring
- `sysex_to_bytearray`: accept strings in ascii hexadecimal notation with no whitespace between bytes
- 20230111

### Refactor

- refactor: switch setup.py to f-strings
- refactor: move send_midi's usage of optparse to argparse
- refactor: introduce pyproject.toml for metadata & optional dependencies
- refactor: remove more python 2 specific code
- refactor: even more python 2 code removed!
- refactor: move function definition out of loop

### Styling

- style: throw send_midi through black & convert to f-strings

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
- fix: deprecated inspect.getargspec() function
- fix: switch to formatargspec() wrapper
- fix: remove blocking of NOTEON messages with zero velocity

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
- doc-html/ build from doc/ with sphinx replaces former www-copy
- docs: add new fields to setup.py

### Features

- feat: implement misc.formatargspec

### Other (unconventional)

- initial import
- git-svn-id: svn+ssh://kobol/srv/svn/mididings@2 5e725e9c-a60a-11dc-ba67-4190e2e3db76
- git-svn-id: svn+ssh://kobol/srv/svn/mididings@3 5e725e9c-a60a-11dc-ba67-4190e2e3db76
- finished renaming midipatch -> mididings
- removed backend.cc
- removed debug parameter from setup/backend
- put util into namespace das
- implemented PythonCall unit
- handle channel/port/program offset in a few more places
- changed python module structure
- updated setup.py
- mostly cleanup
- first attempt at documentation
- simplified backend/setup port parameters
- added MANIFEST
- cleanup
- shouldn't have removed this...
- renamed Types.* to TYPE_*
- allow ProgramChange/ControlChange with one/two parameters
- formatting
- hopefully fixed event processing/routing
- missed one line to clean
- allow passing single patch directly to run/Setup
- renamed _MidiEventEx to MidiEvent
- renamed PatchSwitcher -> PatchSwitch
- shortened unit names
- added Divide()
- preliminary patch switch handling for sustain pedal
- updated "documentation"
- added ProgFilter
- handle multiple sustain pedals
- renamed *.h -> *.hh
- forgot python.cc
- added CtrlValueFilter
- filters now discard other event types
- moved benchmark code from backend_alsa to setup
- new test cases
- removed das::exception, use std::runtime_error instead
- updated unit test
- added example scripts
- added license and README
- allow multiple arguments for Filter
- updated documentation
- updated MANIFEST
- added Setup::sanitize_event() and Sanitize unit
- source tree restructuring:
- added mididings.util.only
- added init_fold example
- added missing files to manifest
- moved Call to unit.*
- moved backend/port parameters from run() to config()
- added 'verbose' parameter
- print patch switch message only if there are at least two patches
- make sure KeySplit and VelocitySplit return Forks, not lists
- make sure init events for the first patch loaded at startup are sent properly
- added start_delay config option
- allow start_delay = 0 to wait for keypress
- updated documentation
- 20080713
- don't allow note on with velocity == 0
- make sure init events of the first patch go through postprocessing
- store only weak reference to Setup, to keep test cases working
- drop events received while waiting for processing to start
- added CallAsync() and CallThread()
- need jack and boost.thread libraries now
- don't call max() on empty sequence
- added python_caller.*, moved code from Call
- mutex code cleanup in PythonCaller
- added PrintString()
- async_thread: lock mutex only before wait()
- release 20080721
- catch exceptions in PythonCaller::call_now()
- added util.py, moved some functions from misc.py
- some code cleanup
- improved Print() indentation, so everything lines up nicely
- major event processing rewrite, retaining the Python-side Chain/Fork structure in C++
- minor naming cleanup
- added remove_duplicates option to config & forks
- changed structure of backend (now engine calls backend, rather than vice versa)
- some more engine/backend cleanup
- more random changes, made too long ago to remember
- just cleanup
- call sanitize again for all outgoing events
- use timed_join() if available (untested)
- yet another change, to compile with boost 1.34.1 again
- added InitAction unit directly to mididings
- updated setup.py (filenames changed)
- make InitAction discard by default
- split units.py into separate files
- reverted filter behavior
- updated test cases
- cleanup
- don't use BOOST_FOREACH during processing, seems to have a negative effect on performance
- cleanup/comments
- remove return value from Patch::process() as well
- don't read map elements after erase
- allow Patch::process() with constant range
- call drop_input() again
- renamed printer.py -> printing.py
- added mididings.units package to setup.py
- corrected version number in setup.py, release 20080817
- added UnitEx, allow Call() to return multiple events
- disable garbage collector
- split PythonCaller::call_now() into smaller functions, cleanup
- typedef Event* in Engine and PythonCaller
- added *Event classes
- added config.hh
- moved to trunk subdirectory
- added mididings.extra module
- updated docs/example for Call()
- added mididings/extra to manifest
- added jack midi backend (asynchronous event processing outside jack process())
- added jack-rt backend (still needs a lot more testing)
- added comparison operators for curious_alloc
- include mididings.extra in install
- moved InitAction to units.base, Output to extra.output
- moved Output back to mididings, it's just too useful to be hidden in extra
- cleaned up import statements... i think. favoring explicit relative imports now
- updated documentation
- allow "dummy" backend
- run all init events through post and sanitize patches. d'oh!
- previous commit was bs. fixed return range of Patch::Extended instead.
- hopefully fixed remove_duplicates
- make use of util.*_number()
- added SendOSC(), SendDBUS() and System()
- added a lot more argument validity checking
- updated docs, added aeolus and klick examples
- added scripts/mididings
- removed scripts/mididings again. it's just too damn ugly
- made BackendJack::process() non-pure virtual, to work around errors when it's called before the object is fully constructed
- updated InitAction doc
- leave negative input velocities to VelocityCurve unchanged
- added basic handling of channel aftertouch
- revert previous commit, commited wrong files
- implemented basic handling of channel aftertouch
- added first_patch and patch_switch_callback parameters to run_patches()
- eliminated Engine::run(), using boost.lambda instead
- added aftertouch support to jack backend
- cleanup
- more comments
- move process thread creation to backend
- make SuppressPC return None/ev instead of True/False
- simplified generators
- restructured JACK backends
- make InvertedFilter a subclass of Filter
- added CtrlSplit, CtrlValueSplit, ProgSplit
- call Engine::run_async() periodically
- updated docs
- added CtrlValueSplit with threshold, changed klick example to use it
- don't discard aftertouch events in sanitize. d'oh!
- added operator // for units
- exception message cosmetics
- mention AFTERTOUCH constant in docs
- improved klick example description
- 20081122
- add bank select support to Output()
- allow patch numbers > 128
- new SMF backend
- updated docs
- added NEWS
- added NEWS entry for 20081123
- added Output() bank parameter to doc
- print error messages if pkg-config can't find packages
- added ignore_types parameter to filter, new operator -
- changed VelocityFilter so that 0 always means "no limit"
- added CallPerChannel()
- updated docs
- updated all copyright dates to include 2009
- release 20090113
- output now supports sending volume changes
- release 20090114
- added polyphony.py to svn. oops
- new compiler options to reduce binary size
- prettier changelog
- made ranges half-open
- don't use relative imports
- some import cleanup
- removed erroneous reference to output_event()
- handle note-on with velocity 0 as note-off (jack/smf backends)
- made Chain a public class, renamed from _Chain
- created sysex branch
- changed html doc font to sans-serif
- make the portname field in print output at least 2 characters wide
- changed the hack to modifiy compiler flags, so it still works on ubuntu jaunty
- preliminary support for scene switching via osc
- added sostenuto parameter to PedalToNoteoff
- the grand renaming: patches are now called scenes, unless they are just patches :)
- added class Scene
- derive Chain from list. let's hope this doesn't break anything, needs more testing after a good night's sleep
- implemented repr() for most units. also, my first metaclass, yay
- removed unit metaclass again, functionality moved to a function decorator
- added misc.call_overload() to simplify units with multiple argument specs
- updated documentation, making sure parameter names match those in the code
- implemented VelocitySlope()
- marked old functions/units as deprecated using the new 'deprecated' decorator
- make use of call_overload() in KeyFilter, VelocityFilter, CtrlValueFilter
- find boost libs whether they have the -mt suffix or not
- cleanup
- removed VelocityCurve() from docs, minor tweaks for next release
- new class _Selector to allow chaining filters using operator % without parentheses
- new class NamedFlag and NamedBitMask for better repr support
- added proper __repr__ for Split
- first attempt at support for system exclusive, system realtime and system common messages
- renamed Call() -> Process() and CallAsync() -> Call()
- split units.hh into multiple smaller files
- added hook system, (re)wrote MemorizeScene, OSCInterface and AutoRestart to use it
- made alsa seq backend optional
- let AutoRestart() automaticall watch imported local modules
- moved config and hooks to new module config
- first version of scripts/mididings
- create a fake entry in sys.modules to make AutoRestart() work
- renamed mididings.units.misc to mididings.units.engine to avoid name conflict with mididings.misc
- unified run() and run_scenes()
- unified Print() and PrintString()
- new ring buffer that can be safely used with C++ objects
- add the directory containing the script to sys.path so import works as expected
- improved documentation and error handling of JACK/ALSA backends
- use Call instead of the deprecated CallAsync
- renamed mididings.config module to mididings.setup to avoid name clash with config() function
- added Route() unit
- changed semantics of CtrlFilter, CtrlValueFilter, ProgFilter and SysExFilter to block events of other types (again)
- changed selector syntax to use new operator &
- import all units directly from mididings/__init__.py, hopefully fixing the crazy modules-with-the-same-name-mix-up problem
- rewritten unit test
- unified Call() and CallThread()
- added event type POLY_AFTERTOUCH (untested)
- removed module main, import selected functions directly from setup and engine
- forgot this one
- replaced PORTNAMES_* flags with simple strings
- import all units into mididings.units, for some reason this seems to work now (?!)
- forgot one again...
- new velocity mode "curve"
- added VelocityLimit()
- added manufacturer id parameter to SysExFilter()
- cleanup
- cleanup and comments
- reverted importing osc, dbus and inotify directly into mididings.extra
- another fix to prevent selecting a nonexisting scene at startup
- note to self: test before commit
- it's 2010, yay
- simplified overloading mechanism by adding overload decorator, and making name parameter to call_overload optional
- renamed InitAction() to simply Init()
- renamed MidiEvent.type_ to MidiEvent.type
- use misc.overload for SysExFilter
- major documentation update
- added basic usage info to mididings script
- more doc fixes
- new release 20100112
- added link to hooks.py
- changed call_overload() to query the name of the calling function only when necessary, resulting in a major performance boost
- remove note-on events with velocity < 1
- added OR selector (operator |)
- added else-rule to splits
- renamed key -> note in KeyFilter() and KeySplit() to keep names somewhat consistent
- more renaming: ProgChange() -> Prog(), CtrlChange() -> Ctrl()
- PROG is PROGRAM again, and all Prog* units were renamed as well
- allow half-open note ranges
- limit printed sysex data to terminal width
- removed types parameter from Fork() and Print()
- take length of Print() name into account when printing sysex
- renamed Note() -> Key()
- unfinished doc update from two weeks ago
- start event type names with uppercase character
- added mididings.extra.LatchNotes()
- more documentation work, removed superfluous examples
- just cleaning up
- minor doc fixes
- updates NEWS for 20100202
- oops
- added extra.Panic()
- added mididings.extra.gm
- made bypass feature of Panic() optional
- replaced for-loops with std::find
- run jack buffered midi processing at realtime priority
- added SceneSwitch(offset)
- import and formatting cleanup
- added support for subscenes
- first commit of livedings
- made custom theme optional and disabled by default
- support wrapping in /mididings/prev_subscene and /mididings/next_subscene
- added package mididings.live to setup.py
- added default arguments to help output
- allow setting initial subscene, save/restore subscene in MemorizeScene()
- replace empty subscene names with (unnamed)
- make OSCInterface accept a single notify port
- support callable objects as parameters to Print(string)
- don't create scene -1
- attempt to fix rare crash when terminating
- added support for multiple individual notes to KeyFilter()
- first commit of FloatingKeySplit()
- turn off sustain pedal in Panic()
- added margin_* parameters to FloatingKeySplit()
- cleanup
- reverted rev 312, seems to make things worse by hanging instead of crashing
- updated documentation
- release 20100307
- support VelocityLimit() with only one limit
- allow Process() functions to return generators
- added VoiceFilter()
- replaced BlackKeys() and WhiteKeys() with KeyColorFilter()
- added OutputTemplate()
- added single-limit versions of VelocityFilter() and CtrlValueFilter()
- updated documentation to include new units
- added engine.restart() and /mididings/restart OSC message
- cleaned up KeyFilter() parameters
- simplified FloatingKeySplit(), don't send superfluous note-offs
- make Engine._restart() static so it doesn't keep a reference to the engine
- don't link to libjack when jack midi is disabled
- don't use operator // in FloatingKeySplit() because it fails with two lists
- added operator +
- eliminated the few remaining relative imports
- updated and improved docs
- updated README/NEWS, release 20100318
- added support for python 3.x, fixed support for python 2.5
- support large sysex message (split into multiple chunks) when using the ALSA backend
- added cstdint include back
- hopefully fixed crash during termination this time, by adding Backend::stop() method
- added SysEx() example
- release 20100413
- added skeleton.py and router.py examples.
- removed some problematic sanity checks when creating MidiEvent objects
- when a scene has subscenes, always print the subscene number when switching scenes
- no need for the commas
- include 64 bit library directories in search for boost libs, and use -mt suffix as fallback
- avoid at least some confusion...
- updated NEWS for 20100508
- changed MidiEvent() parameters to take data_offset into account
- added CtrlCurve() unit
- updated documentation
- release 20100516
- check if backend is null in engine d'tor
- updated documentation
- release 20100602
- minor doc fixes
- use functools.wraps() to keep names of decorated functions intact
- renamed CC# from param to ctrl
- minor doc improvements
- restructured source by moving backends and units to subdirectories
- updated setup.py to reflect code restructuring
- added engine.time() as a monotonic clock source
- make mididings script executable
- moved backend creation from engine to backend/base
- don't use make_shared which isn't available in boost < 1.39.0
- improved VoiceFilter() to work for voices other than highest/lowest
- added license section to README
- replaced -p and -l options with positional arguments (options still supported for backward compatibility)
- changed OSCInterface and livedings to use ports 56418 and 56419 by default
- updated docs to reflect param->ctrl renaming
- release 20101119
- nah, too many line breaks
- removed static (which is deprecated in this context) from functions in Mididings namespace
- it's 2011
- changed default octave_offset to 1
- * removed pass_others parameter from filter base class, assume true for all filters instead.
- return Fork instead of plain list
- * added apply(), invert() and negate() functions
- removed previously deprecated functions
- don't try to import removed functions run_scenes() and run_patches()
- removed deprecated type_ event attribute
- reverted previous accidental commit
- removed deprecated type_ event attribute
- completely reorganized and somewhat extended unit tests
- * added event.SysExEvent()
- added sanity checks for config() parameters
- some improvements to argument checking and error handling in misc and util
- added leading underscore to override and check parameters of setup.config()
- renamed unit test modules to use test_ as a prefix, this way unittest discover does not require additional parameters
- removed DEBUG_FN calls
- made MidiEvent.sysex a property only in python (preparation for python3 string/bytes fixes)
- check sysex data in SysExEvent()
- changed internal representation of sysex data from string to vector<unsigned char>.
- forgot these in previous commit
- add option -n to livedings, allowing each instance to have its own name
- minor documentation changes
- local python3 paths changed
- revert changes to octave_offset and filter behavior (r384 and parts of r385), at least for now
- it's 2012...
- remove ancient sysex branch
- create experimental branch
- add Restart() and Quit() in extra.engine
- some additional documentation, improved formatting, split into smaller files
- more documentation improvements
- change local python3 lib path
- release 20120312
- * automatically disable alsa backend on non-linux platforms, and change default backend to jack if alsa is not available
- still 20120312...
- cleanup
- merge r423 from trunk
- implement proper from/to-python converters for vector types
- add missing (??!!) decref
- some additional type checks
- add MidiEventType <-> int converters
- don't use vector_indexing_suite for testing, use converter instead
- better and cleaner from/to-python converters, moved to src/util
- move overload mechanism to its own module
- remove accidentally commited line
- add unit test for SysExFilter
- * implement regex-based port connection for alsa and jack backends
- minor renaming for consistency
- merge r439 from trunk
- max_size() should apparently return 1, not N
- * convert Patch and related methods to template-based code, to allow different underlying container types
- use custom iterator_range instead of boost's
- more naming cleanup
- add test case for unit execution order
- merge r440:445 (template-based patch processing) from experimental branch
- allow python converters to be compiled with older boost versions which don't support get_pytype()
- save engine args in temporary list for less funny backtraces
- minor cleanup of overload module
- require at least python 2.6
- nah...
- * use python decorator module (new dependency)
- hide basic unit classes behind an underscore, make them available through public functions
- * allow varargs to be used in overloads
- event type and attribute flags now have their own class names
- * NamedBitMask operation return original type for derived classes
- replace variable length array (gcc-ism) with alloca() and placement new
- * clean up/fix sysex data conversion
- this should have been included in the previous commit
- remove unused import
- add missing _unit_repr to SysEx() unit
- SysEx() was broken for data_offset == 1 as well
- * clean up event attribute access
- * more unit tests
- add counted_objects.hh in util
- * use counted_objects base class for engine, module, unit and event types
- * pre-allocate plain bytes instead of default constructed T objects. this avoids using placement new on the location of an existing object.
- allocate plain memory for ring buffer instead of objects of type T, and use placement new to construct objects in the buffer
- optionally print a few memory allocation statistics on module unload
- use nested functions instead of member functions. this fixes a memory leak due to cyclic references (_CallBase -> _mididings.Call -> _CallBase.do_call)
- add test case for Process() using generator
- support docstrings for overload objects
- * add mididings.arguments for argument type checking and conversion
- * more unit tests
- * add port/channel default parameter for Generator()
- prefer inspect.formatargspec() and list/dict __repr__() over DIY stuff
- simplify sequenceof()
- clean up and document arguments.py
- replace file header
- minor formatting changes
- add unit tests for modifiers
- * convert constraints from decorated functions to classes
- * add argument checking for config()
- * make unit tests work again, add tests for arguments.py
- minor formatting changes
- include types of arguments used in overload exception message
- * add repr() support to constraints
- * use shorter list constraint syntax
- * preserve sequence types in sequenceof() and tupleof()
- ensure that initial_scene is a tuple, not a list
- eliminate global pointer to engine, pass a reference as part of the event buffer instead
- * use separate engine wrapper class for virtual function calls
- actually use bitwise or for flags. addition does not necessarily yield the same result!
- * expose midi event types via boost python enum, generate python objects in constants.py automatically
- remove unused enum converters
- * add argument checking for functions in event module
- improved MidiEvent operator equals: only compare the fields which are used by the given event type
- formatting
- much nicer repr() for event types for which utility creation functions exist
- initialize new event from previous one
- don't reject program number 128 (or 127 without data_offset)
- verify that events can be reconstructed from their repr() (for every event returned by every patch, and a couple of random events...)
- prevent local variable from leaking into the mididings module
- * add SYSTEM event type definition
- make sysex events copyable/pickleable
- add @overload.partial, and use it to simplify generator overloads
- default velocity argument for NoteOff()
- argument checking for Scene and SceneGroup
- oops
- again, oops.
- clear globals dict after running script
- * allow None as control/pre/post arguments to run()
- python 3 doesn't have types.NoneType
- * implement python converters from/to shared_ptr<vector>
- adjust backends to use new sysex typedefs
- * add converters to/from python bytes objects
- avoid unnecessary copy of sysex data
- minor cleanup
- use bytearray instead of bytes (and for python 2.6 or later, not just python 3)
- * support manipulating sysex data in-place (in python bytearray, not in C++ vector)
- * remove MidiEvent.param and EVENT_PARAM
- replace "!= None" with "is not None"
- make TransformMode and EventAttribute enums available to python, generate EVENT_* constants automatically
- print asterisks instead of argument types in overload error messages. types are confusing because the overloading mechanism doesn't care about types (yet?)
- unit tests for overload module
- a bit of scene/engine cleanup
- more cleanup
- finally implement port connections on the python side
- * fix printing of sysex events
- * allow make_event() to create sysex events
- make nullable() a regular constraint
- use TransformMode parameters instead of ints
- more python 2.5 fixes, unit tests now work
- watch *all* loaded modules for changes. at least until i find a reliable way to tell which modules are "local" and which aren't
- new and hopefully improved logic to figure out which modules to watch for changes
- * add mappingof() constraint
- * add (stricter) typechecking for splits
- bypass the overload mechanism if a dict is passed to run() that is not a valid split
- forgot to make Split() key nullable
- don't call getargspec() when units are created, but only when their repr() is needed
- cache all results of inspect.getargspec() to improve performance
- another tiny performance boost, @accept is now a class
- run unit tests before committing...
- make type and value constraints separate classes, avoid expensive calls to isinstance() and inspect.isclass() during argument checking
- parse portnames when the config changes, not every time engine.in_ports() and engine.out_ports() are called
- retrieve port names directly from setup
- rename Engine.process_test() to process_event(), and always include it in mididings builds
- * add -I and -O options to scripts/mididings to specify port connections
- split core.html into core.html and units.html
- change port connection config data structure to a single variable-length sequence containing both port name and all connections
- release 2012-04-19
- change link to decorator module
- updated and improved logic to find out boost library names
- add support for exit patches, probably fixing a bug handling non-list init patches along the way
- support "else clause" for selectors using 2-tuple notation. needs more testing
- add docstring for PerChannel
- preparation for implementing check_sequence() helper function
- more generic to/from python converters, split into multiple header files
- add build directory and .sconsign.dblite to svn:ignore
- use std::atomic_size_t instead of glib functions if c++11 is enabled
- use integer division to ensure that FloatingKeySplit() behaves the same with all python versions
- add --enable-c++11 option to setup.py, defaulting to False
- attempt to reduce stack size of async and jack backend threads if boost 1.50 or later is used
- cleanup and more comments in config.hh, changed int to std::size_t where appropriate
- minor useless cleanup
- add Transpose(octaves=...)
- update copyright date
- add converters to/from bytes, and combine converters for bytes and bytearray in one header
- change namespace names to all lowercase
- add finish() method to backend interface, and implement it for JACK realtime backend
- add send_midi() function
- undo accidental changes
- remove unneeded static keyword from config constants
- define program version only at one place in setup.py
- add unfinished version of send_midi script
- discard sysex data not starting with 0xf0, rather than crashing
- don't try to start JACK server if it's not already running
- slightly more verbose error messages when regexes don't match any ports
- working implementation of send_midi
- add send_midi to the scripts to be installed
- #include <boost/version.hpp> before checking BOOST_VERSION.
- add das::python::scoped_gil_release
- add SND_SEQ_PORT_TYPE_MIDI_GENERIC to alsa ports, thanks to Oleg Samarin.
- update copyright dates
- copy boost library name detection from setup.py
- move trunk to top level, delete svn branches
- add .gitignore
- update compiler warning flags
- cleanup
- Merge branch 'master' of ssh://kobol/srv/git/mididings
- drop support for python 2.5
- cleanup
- drop support for boost versions before 1.37.0
- don't terminate python caller if there's still stuff to do
- support constraints for keyword arguments with unspecified names
- allow additional arguments to Process(), Call(), etc.
- add _Unit.add() method, for completeness' sake
- properly support polyphonic aftertouch
- remove python 2.5 compatibility cruft
- move buffer<->MidiEvent conversion out of backend class
- expose buffer<->MidiEvent conversion to python
- remove smf backend, add replacement using pysmf
- update requirements in readme
- no need for import from __future__
- don't attempt to set rt priority of less than 1
- order events from all JACK input ports by frame
- support callable objects in Call() and Process()
- keep mididings.extra module namespace clean
- generate documentation using sphinx
- combine units in a single document
- allow types to be used in patches directly
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
- highlight current document in sidebar
- add documentation of livedings and send_midi
- update unit tests now that Call() has changed
- clean up SConstruct
- remove python 2.5 compatibility cruft
- make Fork() and Chain() accept varargs
- add varargs automatically instead of using *rest
- manually set docstring when using add_varargs
- don't use code::, add newlines after note::
- reformat code to 80 columns
- reformat SConstruct to 80 columns as well
- reduce size of fixed width font a little more
- set __name__ of data_offset_wrapper
- don't use boost.lambda; minor cleanup
- prettier formatting of allocation stats
- add /core to .gitignore
- update curious_alloc for C++11
- rework benchmark code, print results on unload
- relax parameter checking of *Event() functions
- allow engine with no input or output ports
- make das::regex default-constructible and copyable
- ignore unmatched note off events in VoiceFilter()
- add mididings -p option for a simple event logger
- define BOOST_PYTHON_NO_PY_SIGNATURES
- optimize compiler flags, remove default libdirs
- minor formatting and comments
- expose backend creation to Python
- add mididings interactive shell (option -s or -S)
- include git revision in version information
- only try to execute valid mididings patches
- command line options for data and octave offset
- support user config file
- clearer error message
- implement stop() properly to prevent segfault
- more documentation for mididings command line tool
- add mididings.extra.CtrlToSysEx()
- support indented multi-line input
- support reattaching to jack buffered backend
- Use boost::unordered_map, fix build issues on OSX
- rename sysex_to_sequence() to sysex_to_bytearray()
- support SysEx strings in ASCII notation
- use offset() instead of NoDataOffset()
- allow port/channel of Output() to be omitted
- Try to use setuptools, fall back to plain distutils
- Add encoding declaration to allow non-ascii chars in metadata
- Ensure compiler output is in C locale
- convert images to indexed colors
- add some more examples to documentation
- print actual sysex data value that's out of range
- clarify documentation regarding scene numbers
- validate scene numbers, fix run() argument checking
- implement Key() as a single unit in C++
- update .gitignore
- include git rev in version number passed to setuptools
- scene -> subscene mispell
- curious_alloc: fix template version of destroy()
- harmonizer: fix integer division
- call: use asyncFlag instead of async
- Add Arch Linux PKGBUILD
- jack: use inverse logic in connect_matching_ports
- jack: further simplifications
- jack: Add support for jack alias names
- setup for python3-install
- Update README
- html-doc for mididings from original www-pages
- Explain fix for missing boost_python
- more python3 related updates
- Copied the web site
- Update README
- Update README
- Update README
- Update README
- Update README
- Update README
- Update README
- Moved the assignment of current_patch, current_scene and current_subscene before init patch processing so when calling current_scene() from an init patch it returns the correct scene and not the previous one.
- Fix boost_python_suffixes to match format of boost_python libraries

### Performance

- perform type checking in operators >>, // and %

### Refactor

- refactor ALSA port connecting
- refactor: remove PKGBUILD
- refactor: remove unnecessary scripts
- refactor: remove unnecessary documentation
- refactor: fix boost deprecation
- refactor: fix PyEval_InitThreads() deprecation
- refactor: remove python 2 specific code
- refactor: delete documentation build directory

### Styling

- style: set setup.py permissions to 0644

### Testing

- test cases for event copy and pickle

<!-- generated by git-cliff -->
