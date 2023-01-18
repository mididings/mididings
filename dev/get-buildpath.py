#!/usr/bin/env python3

import platform
import os

# python -m build creates temporary directories when building the package,
# we can use these temporary directories instead of installing the package
# afterwards.

cwd = os.getcwd()
system = platform.system().lower() # linux
arch = platform.machine() # x86_64
impl = platform.python_implementation().lower() # cpython
pyver = "".join(map(str, platform.python_version_tuple()[:2])) # 310

path = f"{cwd}/build/lib.{system}-{arch}-{impl}-{pyver}" # $PWD/build/lib.linux-x86_64-cpython-310

print(path)
