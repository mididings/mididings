import os
import re

from _mididings import __version__

def open_and_extract(filepath, regex, line_match):
    with open(filepath) as input_file:
        lines = input_file.readlines()

        for line in lines:
            if line.startswith(line_match):
                match = regex.match(line)

                if match:
                    return match.group(1)

class TestVersion:
    def test_versions_match(self):
        version = None
        documentation_version = None
        mididings_version = None

        meson_ver = re.compile(r".*version *: *'([^']*)'")
        doc_ver = re.compile(r"version = \"(.*)\"")
        pyproject_dyn_ver = re.compile(r"(dynamic) *= *\[.*'version'.*\]")

        version = open_and_extract("meson.build", meson_ver, "project")
        documentation_version = open_and_extract("doc/conf.py", doc_ver, "version")
        mididings_version = __version__
        pyproject_version = open_and_extract("pyproject.toml", pyproject_dyn_ver, "dynamic")

        assert version is not None
        assert documentation_version is not None
        assert mididings_version is not None
        assert version == documentation_version
        assert version == mididings_version
        assert pyproject_version == "dynamic"

