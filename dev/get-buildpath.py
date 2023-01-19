#!/usr/bin/env python3

import platform
import os

# python -m build creates temporary directories when building the package,
# we can use these temporary directories instead of installing the package
# afterwards. the format of this path is as follows:
# $(pwd)/build/lib.linux-x86_64-cpython-310

cwd = os.getcwd()
system = platform.system().lower()
arch = platform.machine()
impl = platform.python_implementation().lower()
pyver = "".join(map(str, platform.python_version_tuple()[:2]))

print(f"{cwd}/build/lib.{system}-{arch}-{impl}-{pyver}")
