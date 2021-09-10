#!/bin/sh
# This is an exampe script, to install all packages and run the build and install process

sudo apt --yes install libglib2.0-dev libjack-jackd2-dev
sudo apt --yes install libboost-python-dev libboost-thread-dev
sudo apt --yes install python3-liblo python3-dbus python3-decorator python3-pyinotify python3-tk 

python3 setup.py build

sudo pip install dist/mididings-*.whl
