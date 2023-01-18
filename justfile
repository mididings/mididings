#!/usr/bin/env -S just --justfile
# ^ A shebang isn't required, but allows a justfile to be executed
#   like a script, with `./justfile test`, for example.

build-dir := `python dev/get-buildpath.py`

# list all recipes by default
default:
  just --list

# clean everything
clean: clean-pycache clean-build clean-manpages clean-documentation

# delete python cache artifacts
clean-pycache:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name __pycache__ -delete

# delete distribution artifacts
clean-build:
  rm --force --recursive build dist *.egg-info

# delete generated man pages
clean-manpages:
  rm -rf doc/man/*.1

# delete generated documentation
clean-documentation:
  rm -rf doc/build

# build sdist & wheel
build: build-wheel build-sdist

# build wheel artifact with python -m build
build-wheel: build-manpages
  python -m build --no-isolation --wheel

# build sdist artifact with python -m build
build-sdist: build-manpages
  python -m build --no-isolation --sdist

# generate documentation with sphinx
build-documentation: build-wheel
  PYTHONPATH={{build-dir}} sphinx-build -b html -d doc/build/doctrees doc doc/build/html

# generate reproducible man pages with scdoc
build-manpages:
  #!/usr/bin/env bash
  pushd doc/man > /dev/null
    for script in livedings mididings send_midi; do
      scdoc < "${script}.scd" > "${script}.1"
    done
    bash reproducible-man.sh
  popd > /dev/null

# run test suite with pytest
test: build-wheel
  PYTHONPATH={{build-dir}} pytest -v 

# validate licensing information with reuse
lint-licensing:
  reuse lint

# lint python source code with ruff
lint-python:
  ruff mididings tests

# lint cython source code with cppcheck
lint-cython:
  cppcheck src

# lint all markdown documentation with mdl
lint-markdown:
  mdl .
