import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import yaml
import rally_connector
import google_connector

#Initialize the Google connector
g = google_connector.g("1eB_amBkQKIU58ivzJ4Yyqefhc1XPWbTQ4BDtHdSJKba", "Form Responses")

#Initialize the Rally connector
with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

url = config['rally']['url']
apikey = config['rally']['apikey']
workspace = config['rally']['workspace']
project = config['rally']['project']
logging = config['rally']['logging']

r = rally_connector.r(url, apikey, workspace, project, logging)

#Get full Google Sheet, then find new rows
full_sheet = g.getGoogleSheet()
old = pd.read_csv("old.csv")
sheet = g.getNewRows(full_sheet, old)

print ("Here are the new row(s):")
print (sheet)

#For each new row, load columns into a Rally description
for i, row in sheet.iterrows(): 
    description=""
    for x, y in row.iteritems():
        description = description + "<b>" + str(x) + ":</b> " + str(y) + "<br>"
    
    #Create feature in Rally
    feature_name = row["Asset title"]
    reqinfo = {'Name':feature_name, 'Description':description}
    rally = r.setFeature(reqinfo)

    print ("The new feature number is: " + rally.FormattedID)

#Write the original sheet to the original file
full_sheet.to_csv("old.csv")