"""Done Grading Script

This script will click "Done Grading" for all submitted exams for an event.

Make sure scoring is unlocked before running. It may be a good idea to back up
the scores before running this script.
"""

from twill import browser
from twill.commands import *
import twill
import os
import dotenv
import re
import time
import sys

dotenv.load_dotenv(dotenv_path='../.env')

# Send all twill output to /dev/null
null = open(os.devnull, 'w')
twill.set_output(null)

SCILYMPIAD_BASE = os.getenv('SCILYMPIAD_BASE_URL')
DIVISION = os.getenv('DIVISION')
go(SCILYMPIAD_BASE)
follow('Log in')
fv(1, "Email", os.environ['SCILYMPIAD_USERNAME'])
fv(1, "Password", os.environ['SCILYMPIAD_PW'])
submit(6)
# should be on main page now
follow('ES')
# Use the switcher:
go(os.getenv('SCILYMPIAD_EVENT_SWITCHER_URL'))

links = showlinks()
# Extract links for each button in the switcher
event_links = [l for l in links if 'Division: ' in l.text]

event_name = input('Event to click "Done Grading" for: ')
event_to_change = None
for l in event_links:
    if event_name in l.text:
        event_to_change = l
if event_to_change is None:
    print('Did not find event {}. Make sure the spelling matches that on Scilympiad'.format(event_name))
    exit()

follow(event_to_change.text)
follow('Grade Online Tests')
grading_links = showlinks()
for l in grading_links:
    if 'selTeam' in l.url:
        # Extract team number
        team_no = re.findall(r'"({}[0-9]*)"'.format(DIVISION), l.url)
        if len(team_no) != 1:
            print('Invalid team name extraction {} for url {}'.format(team_no, l.url), file=sys.stderr)
            continue
        else:
            team_no = team_no[0]
        # Extract test id
        tid = re.findall(r'\(\"([0-9A-Z]*)\"', l.url)
        if len(tid) != 1:
            print('Invalid tid extraction {} for url {}'.format(tid, l.url), file=sys.stderr)
            continue
        else:
            tid = tid[0]
        
        # Send command to Done Grading endpoint
        url = '{}/Es/DoneGrade?tid={}&tno={}'.format(SCILYMPIAD_BASE, tid, team_no)
        print('Clicking Done Grading for tid {}, team {}'.format(tid, team_no), file=sys.stderr)
        go(url)
        time.sleep(0.1) # rate-limiting



null.close()
