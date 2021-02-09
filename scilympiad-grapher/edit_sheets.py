""" Google Sheets Updater

This script uses the Google Sheets API to update a spreadsheet

Follow the instructions here (https://developers.google.com/sheets/api/quickstart/python) 
before running the code to get credentials.json.
"""

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import dotenv

dotenv.load_dotenv(dotenv_path='../.env')

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
RANGE = os.getenv('SPREADSHEET_RANGE')

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)


    # Call the Sheets API for writing
    with open('stats.csv', 'r') as f:
        values = f.readlines()
    values = [row.strip().split(',') for row in values]
    values = [[int(j) for j in i] for i in values] # should be 22 x 4

    data = [
        {
            'range': RANGE,
            'values':values
        }
    ]
    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': data
    }
    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body=body
    ).execute()

    print('{0} cells updated.'.format(result.get('totalUpdatedCells')))


if __name__ == '__main__':
    main()
