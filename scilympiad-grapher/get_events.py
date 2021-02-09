"""Scilympiad Events Scraper

This script extracts the breakdown of exam statuses for each event over the
course of the tournament.

This tool outputs a file called stats.csv which lists the number of graded,
in-progress, ungraded (but completed), and time-extended exams. The rows are 
given in the same order as they are stored in Scilympiad.
"""

from twill.commands import *
import twill
import os
import dotenv
import sys
import time

dotenv.load_dotenv(dotenv_path='../.env')

# Send all twill output to /dev/null
null = open(os.devnull, 'w')
# Comment out the next line to use print statements for debugging
# or use print('some_output_text', file=sys.stderr)
twill.set_output(null)

go(os.getenv('SCILYMPIAD_BASE_URL'))
follow('Log in')
# For some reason, Twill names the login-form as Form 2, but you need to 
# subtract one before using the fv function.
# There is no mention of this in the documentation...
fv(1, "Email", os.getenv('SCILYMPIAD_USERNAME'))
fv(1, "Password", os.getenv('SCILYMPIAD_PW'))
submit(6)
# should be on main dashboard now
follow('ES')
# Use the switcher:
go(os.getenv('SCILYMPIAD_EVENT_SWITCHER_URL'))

links = showlinks()
# Find all event buttons within the switcher
event_links = [l for l in links if 'Division: ' in l.text]
with open('stats.csv', 'w') as f:
    for i in range(len(event_links)):
        follow(event_links[i].text)
        follow('Grade Online Tests')
        html = show()
        # Instead of parsing the HTML, we just count the number of tags of each color
        graded_exams = html.count('<tr class="w3-food-kiwi">')
        in_progress_exams = html.count('<tr class="w3-food-orange">')
        ungraded_exams = html.count('<tr class="w3-food-lemon">')
        time_extension = html.count('<tr class="w3-food-salmon">')
        f.write('{},{},{},{}\n'.format(graded_exams, ungraded_exams, in_progress_exams, time_extension))
        # Return to the event switcher
        back()
        back()
        time.sleep(0.1) # probably a good idea to rate limit just a bit

null.close()
