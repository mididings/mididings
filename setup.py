#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import platform
import sys
import sysconfig

from subprocess import getstatusoutput
from setuptools import setup, Extension


def extract_version():
    """
    Extract version from pyproject.toml.

    This exists so pyproject.toml is the single source of truth for the
    package version.
    """
    # initialise with placeholder
    version = "dev"

    # compile regexp
    regexp = re.compile(r"version = \"(?P<version>\d*)\"")

    # open pyproject.toml
    with open("pyproject.toml") as input_file:
        lines = input_file.readlines()

    # extract version
    for line in lines:
        if line.startswith("version"):
            match = regexp.match(line)

            if match:
                version = match.group("version")
                break

    return version


version = extract_version()

config = {
    'alsa-seq':     (platform.system() == 'Linux'),
    'jack-midi':    True,
    'debug':        False,
}

# information for compiled extension
sources = [
    "src/engine.cc",
    "src/patch.cc",
    "src/python_caller.cc",
    "src/send_midi.cc",
    "src/python_module.cc",
    "src/backend/base.cc",
]
library_dirs = []
include_dirs = ["src"]
libraries = []
define_macros = [("VERSION", f"{version}")]


def pkgconfig(name):
    """
    Run pkg-config for the given package, and add the required flags to our
    list of build arguments.
    """
    status, output = getstatusoutput(f"pkg-config --libs --cflags {name}")
    if status:
        sys.exit(f"couldn't find package '{name}'")
    for token in output.split():
        opt, val = token[:2], token[2:]
        if opt == "-I":
            include_dirs.append(val)
        elif opt == "-l":
            libraries.append(val)
        elif opt == "-L":
            library_dirs.append(val)


def library_path_dirs():
    """
    Extract library paths from LIBRARY_PATH environment variable.
    """
    library_path = os.environ.get("LIBRARY_PATH")
    return library_path.split(":") if library_path else []


def lib_dirs():
    """
    Attempt to return the compiler's library search paths.

    Also include paths from LIBRARY_PATH environment variable.
    """
    env_libs = library_path_dirs()
    try:
        status, output = getstatusoutput(
            "LC_ALL=C " + sysconfig.get_config_var("CC") + " -print-search-dirs"
        )
        for line in output.splitlines():
            if "libraries: =" in line:
                libdirs = [
                    os.path.normpath(p) for p in line.split("=", 1)[1].split(":")
                ]
                return env_libs + libdirs
        return env_libs
    except Exception:
        return env_libs


def boost_lib_name(name, add_suffixes=[]):
    """
    Try to figure out the correct boost library name (with or without "-mt"
    suffix, or with any of the given additional suffixes).
    """
    libdirs = lib_dirs()
    for suffix in add_suffixes + ["", "-mt"]:
        for libdir in libdirs:
            for ext in ["so"] + ["dylib"] * (sys.platform == "darwin"):
                libname = f"lib{name}{suffix}.{ext}"
                if os.path.isfile(os.path.join(libdir, libname)):
                    return name + suffix
    return name


libraries.append(
    boost_lib_name("boost_python", [f"{sys.version_info[0]}{sys.version_info[1]}"])
)
libraries.append(boost_lib_name("boost_thread"))

library_dirs.extend(library_path_dirs())

if config["alsa-seq"]:
    define_macros.append(("ENABLE_ALSA_SEQ", 1))
    sources.append("src/backend/alsa.cc")
    pkgconfig("alsa")

if config["jack-midi"]:
    define_macros.append(("ENABLE_JACK_MIDI", 1))
    sources.extend(
        [
            "src/backend/jack.cc",
            "src/backend/jack_buffered.cc",
            "src/backend/jack_realtime.cc",
        ]
    )
    pkgconfig("jack")

setup(
    ext_modules=[
        Extension(
            name="_mididings",
            sources=sources,
            include_dirs=include_dirs,
            library_dirs=library_dirs,
            libraries=libraries,
            define_macros=define_macros,
        ),
    ],
    packages = [
        'mididings',
        'mididings.units',
        'mididings.extra',
        'mididings.live',
    ],
    scripts = [
        'scripts/mididings',
        'scripts/livedings',
        'scripts/send_midi',
    ],
    data_files=[
        (
            "share/man/man1",
            [
                "doc/man/mididings.1",
                "doc/man/livedings.1",
                "doc/man/send_midi.1",
            ],
        ),
    ],
)
