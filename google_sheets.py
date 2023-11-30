from __future__ import print_function
import pickle
import telebot
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from telebot import types


class GoogleSheet:
    SPREADSHEET_ID = '1_-_tJAjUZaVonU6UsR3S8mCZw8jtlQ4Bm2zk9B574Ws'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = None

    def __init__(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

    # функции не называют с большой
    def updateRangeValues(self, range, values):
        # body = {
        #     'valueInputOption': 'USER_ENTERED',
        #     'data': [{
        #         'range': range,
        #         'values': values
        #     }]
        # }
        data = [{
            'range': range,
            'values': values
        }]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID,
                                                                  body=body).execute()
        # Вывести в логи https://habr.com/ru/companies/wunderfund/articles/683880/
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))

    def add_nylist(self, list_name):
        body = {'requests': [{'addSheet': {'properties': {'title': list_name}}}]}
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
        print(f"Added new list {list_name}")


# Возможно добавить в класс
def sheet_adding(ListName, StartCord, EndCord, DriverName, CarName, Value, Plomba, DataTime):
    # Описать в конструкторе класса
    gs = GoogleSheet()
    test_range = f'{ListName}!A{StartCord}:E{EndCord}'
    test_values = [
        [DriverName, CarName, Value, Plomba, DataTime],

    ]
    gs.updateRangeValues(test_range, test_values)

# def get_data(DataTime, DriverName, CarName, ListName, EndCord):
#     gs = service
#     get_range = f'{ListName}!A{2}:E{EndCord}'
#     gs.va
