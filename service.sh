#!/bin/bash
#source /home/npascual/code/.env/bin/activate
if [ -n "${VIRTUAL_ENV:-}" ] ; then
	#source /home/npascual/code/.env/bin/activate
    echo "Env already loaded."
else
    source /home/npascual/code/.env/bin/activate
fi
# source /home/npascual/code/.env/bin/activate
cd /home/npascual/code/sensehat-mqtt
python publish.py 
#exit 0
