import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe

class g:

    def __init__(self, docid, worksheet_name):
        self.docid = docid
        self.worksheet_name = worksheet_name
        
        print ("Logging into Google.")
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
        client = gspread.authorize(credentials)
        sh = client.open_by_key(self.docid)
        self.worksheet = sh.worksheet(self.worksheet_name)

    def setGoogleSheet(self, data):
        print ("Uploading Google Sheet.")
        set_with_dataframe(self.worksheet, data)

    def blankGoogleSheet(self):
        print ("Blanking Google Sheet.")
        sheet = self.worksheet.get_all_values()

        headers = sheet.pop(0)
        sheet = pd.DataFrame(sheet, columns=headers)

        length = len(sheet.index)+1

        cells = "A1:Y" + str(length)

        cell_list = self.worksheet.range(cells)
        for cell in cell_list:
            cell.value = ""

        self.worksheet.update_cells(cell_list)

    def getGoogleSheet(self):
        print ("Downloading Google Sheet.")
        #Get Form Responses tab as a list of lists
        sheet = self.worksheet.get_all_values()

        #Convert sheet to dataframe
        headers = sheet.pop(0)
        sheet = pd.DataFrame(sheet, columns=headers)

        return sheet

    def getNewRows(self, new, old):
        print ("Getting new rows.")
        return new[~new.index.isin(old.index)]