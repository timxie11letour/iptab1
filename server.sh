#!/bin/sh -e

set -x

BASE=${1}
if [ -z $BASE ]; then
	BASE=$(pwd)
fi

export PYTHONPATH=$BASE
nohup python server.py &