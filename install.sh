#!/bin/sh
# This is an install script, to install all packages, clone the reposiory and run the build and setup process

sudo apt --yes install libglib2.0-dev libjack-jackd2-dev
sudo apt --yes install libboost-python-dev libboost-thread-dev
sudo apt --yes install python3-liblo python3-dbus python3-decorator python3-pyinotify python3-tk 

# git clone  https://github.com/dsacre/mididings.git # original repository, but problems with python >3.7
# git clone  https://github.com/rralf/mididings.git # fork which works for python 3.7, scripts are python2 
git clone  https://github.com/rodisch/mididings.git # fork scripts set to python3 

# fix missing -lboost_python
cd /usr/lib/x86_64-linux-gnu
sudo ln -s libboost_python38.so libboost_python.so

cd mididings
sudo python3 setup.py build
sudo python3 setup.py install

