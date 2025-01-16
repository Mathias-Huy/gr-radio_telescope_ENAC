#!/usr/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir="/home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC"
export GR_CONF_CONTROLPORT_ON=False
export PATH="/home/mathuy/gr-radio_telescope_ENAC/build/python/radio_telescope_ENAC":"$PATH"
export LD_LIBRARY_PATH="":$LD_LIBRARY_PATH
export PYTHONPATH=/home/mathuy/gr-radio_telescope_ENAC/build/test_modules:$PYTHONPATH
/usr/bin/python3 /home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC/qa_Save.py 
