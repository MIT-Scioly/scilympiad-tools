#! /bin/bash

cd ABSOLUTE_PATH_TO_PROJECT_DIRECTORY
source venv/bin/activate
cd scilympiad-grapher
python get_events.py
python edit_sheets.py

# Uncomment the following line to save persistent time-stamped logs
# cp stats.csv logs/stats-$(date +%Y-%m-%d-%H-%M-%S).csv
