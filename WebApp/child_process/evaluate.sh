#!/bin/sh
DIR="$( cd "$( dirname "$0" )" && pwd )"
source "${DIR}/venv/bin/activate"
STDOUT=$(python "${DIR}/run_model.py" "$1")
deactivate
echo "${STDOUT}"