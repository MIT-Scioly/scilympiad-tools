# Scilympiad Tools

This is a collection of scripts that was used by MIT Science Olympiad during the 2021 Invitational to help with the use of Scilympiad.

Included are two projects:

- `click-done-grading`: clicks the "Done Grading" button on every exam submitted for a particular event.
- `scilympiad-grapher`: graphs the progress of exam submission and grading by scraping the ES grading pages.

## Description

These scripts all rely on the Twill package which allows for easy interfacing with Scilympiad and avoids the problems of figuring out how session credentials are stored.

### `click-done-grading`

This script clicks the "Done Grading" button for all exam submissions in a particular event. This addresses a problem we discovered during grading after events used horizontal grading, but because the "Done Grading" button was not clicked after everyone had finished, the final scores were not summed correctly (i.e. some grading changes had not been included in the final score).

Scilympiad uses a URL endpoint to indicate "Done Grading" for a particular exam which requires the test ID and the Team Number. This script extracts both parameters and formats the URL correctly. Note that we do not blindly access this endpoint for all teams because clicking "Done Grading" for a team that has not submitted an exam has undefined behavior. To avoid introducing any internal errors, we use Twill to grab the list of all submitted exams and only click "Done Grading" on those exams.

Before running this script for a particular event, make sure that the Event Supervisor did not manually enter scores for each event in the "Event Scoring" page on Scilympiad (i.e. the screen used to break ties and assign tiers). Done Grading will overwrite the values in the Score1 column with the scores summed from the exams. We have observed that Tie Breakers and Tiers are preserved. Export the scores first if you are not sure.

We recommend also using this script to check that "Done Grading" has been clicked on all exams that used Scilympiad's built-in grading system. To do this, for each event, we exported the initial scores as Excel, ran the done grading script for that event, exported the scores again as Excel, converted both to CSV, and fed the two CSVs through `diff` to see if any scores changed. If they did, then the ES needs to be contacted to review the changes.

### `scilympiad-grapher`

This code adds a script that uses the Google Sheets API to update a spreadsheet. `get_events.py` outputs a CSV containing the status of the exams for all events. `edit_sheets.py` updates a spreadsheet with the data from this CSV.

While not the most programatically elegant, this allows for high flexibility and ease-of-use: you can just grab the CSV and parse it yourself if you'd like. Also, plotting with Google Sheets allows for easy graph customization and publishing. A link can simply be distributed to ES's to share the graph.

## Disclaimer

All code is presented as-is without any guarantees of functionality or correctness. You are free to use the code however you like, but it is at your own risk.

Before running the scripts, a couple things to keep in mind:

- This was a small project made during the tournament. Bugs are likely!
- Scilympiad is under very active developement with links and functionality changing constantly. This code may break at any time. Also, it's possible that updates to Scilympiad will make this code obsolete!
- All the tools here make automated, repeated requests to Scilympiad. Though it's unlikely you would do so accidentally, please don't modify this code to intentionally try to DOS the site!

## Setup

### General Setup

These steps are required to use all the tools included

1. Get a Scilympiad account, and add yourself as an ES to each event.
2. Set up your environment file.
   - Take a look at `sample.env`
   - Copy the contents with the fields filled in to a file named `.env`
   - Your `.env` will contain private information. Do not commit this to source control.
3. It is recommended that you run this code within a virtual environment. We recommend virtualenv.

    ```bash
    # Create a virtual environment named venv and activate it
    python3 -m venv venv
    source venv/bin/activate
    # Install all requirements
    pip install -r requirements.txt

    # Note: you should run everything above inside the virtual environment, but 
    # you can use the following command to exit the venv:
    deactivate
    ```

You should be able to run `click_done_grading` at this point with `python click_done_grading/click_done_grading`

### Scilympiad Grapher Setup

The following steps are needed to set up the grapher and monitor.

1. Create a Google Sheets spreadsheet to plot the results with.
2. Set up credentials for the Google Sheets API for `edit_sheets.py` to work
   1. Download 'credentials.json' from [this page](https://developers.google.com/sheets/api/quickstart/python) at "Enable the Google Sheets API".
   2. Put `credentials.json` into the `scilympiad-grapher` directory.
   3. If you are running this for the first time on a headless machine, you may need to run `edit_sheets.py` first on a local machine with a GUI in order to generate `token.pickle`. This token can then be moved onto the headless server to grant access to your Google Sheets spreadsheet.
3. Update the `update_graph.sh` script with the current working directory of this project.
   1. Run `pwd` in your project directory.
   2. Paste this output into the shell script where it says `ABSOLUTE_PATH_TO_PROJECT_DIRECTORY`
4. Do a dry run with `./update_graph.sh`. You should see an indication on your spreadsheet that you have updated the sheet.
5. If the above step works, set up a cronjob to run the shell script periodically (`crontab -e`). The following crontab sets the script to run every 3 minutes.

    ```bash
    SHELL=/bin/bash

    */3 * * * * /absolute/path/to/update_graph.sh
    ```

## Getting Help

If you need help getting these scripts to work, feel free to open an issue on Github. Alternatively, you can email scioly@mit.edu.

## Contributing

Pull requests are welcome, but we make no guarantees about actively maintaining this project.

If you add any new code that uses new packages, please update `requirements.txt` with `pip freeze > requirements.txt` (assuming you are developing within the virtual environment.)

## Acknowledgements

Special thanks to Matthew Cox (2021 Circuit Lab supervisor) from MIT for his contributions to the Done Grading scripts.
