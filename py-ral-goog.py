import rally_connector
import google_connector
import click
import yaml
import pandas as pd
import json
import ast

@click.command()
@click.option('--config-file', default='config.yaml', help="If you don't use the default config.yaml settings file, specify an alternative filename by using this setting.")
@click.argument('action')
@click.option('--getfields', help="When fetching user stories, specify what fields you would like to download.")
@click.option('--setfields', help="When setting user stories, specify what fields you would like to upload.")
@click.option('--us', help="Specify a user story number.")
@click.option('--f', help="Specify a feature number.")
@click.option('--docid', help="Specify a Google doc.")
@click.option('--tab', help="Specify a tab in a Google doc.")
@click.option('--file', help="Specify a tab in a Google doc.", default="file.csv")

def run(config_file, action, getfields, setfields, us, f, docid, tab, file):
    # load the config file
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)

    url = config['rally']['url']
    apikey = config['rally']['apikey']
    workspace = config['rally']['workspace']
    project = config['rally']['project']
    logging = config['rally']['logging']

    # create rally instance
    r = rally_connector.r(url, apikey, workspace, project, logging)

    # parse fields
    if getfields:
        getfields = getfields.split(",")
    else:
        getfields = []

    if setfields:
        setfields = ast.literal_eval(setfields)

    # program actions start here
    # for example: python3 py-ral-goog.py getBoard --fields MRM,RequestedBy
    if action.lower() == 'getboard':
        data = r.getBoard(getfields)
        print (data)
        print ("Now writing the user story information to " + file)
        data.to_csv(file)


    # for example: py-ral-goog.py getUserStory --us US204619
    elif action.lower() == 'getfeature':
        data = r.getFeature(f)
        print (data.details())

    # for example: py-ral-goog.py getUserStory --us US204619
    elif action.lower() == 'getuserstory':
        data = r.getUserStory(us)
        print (data.details())

    # for example: py-ral-goog.py getTasks --us US204619
    elif action.lower() == 'gettasks':
        data = r.getTasks(us)
        for task in data:
            print (task.details())

    # for example: python3 py-ral-goog.py setFeature --fields "{'Name':'Testing123', 'Description':'DeleteMe'}"
    elif action.lower() == 'setfeature':
        data = r.setFeature(setfields)
        print ("Here is the new feature number: " + data.FormattedID)

    # for example: python3 py-ral-goog.py setUserStory --fields "{'Name':name,'PortfolioItem':'306647602476','Description':'TextHere','Language':'ES','RequestedBy':'NameHere'}"
    elif action.lower() == 'setuserstory':
        data = r.setUserStory(setfields)
        print ("Here is the new user story number: " + data.FormattedID)

    # for example: python3 py-ral-goog.py setTask --fields "{'Name':'NameHere','WorkProduct':}"
    elif action.lower() == 'settask':
        data = r.setTask(setfields)
        print ("Here is the new task number: " + data.FormattedID)

    # for example: python3 py-ral-goog.py getGoogleSheet --docid 1XvG7yLFmNPWrRUF_bifos-slAQo2ieuVBcHo8LNVUn0 --tab Frontend --file file.csv
    elif action.lower() == 'getgooglesheet':
        g = google_connector.g(docid, tab)
        data = g.getGoogleSheet()
        print ("Now writing the Google Sheet to " + file)
        data.to_csv(file, index=False)

    # for example: python3 py-ral-goog.py setGoogleSheet --docid 1XvG7yLFmNPWrRUF_bifos-slAQo2ieuVBcHo8LNVUn0 --tab Frontend --file file.csv
    elif action.lower() == 'setgooglesheet':
        g = google_connector.g(docid, tab)
        df = pd.read_csv(file)
        g.setGoogleSheet(df)
        print ("Now uploading data to the Google Sheet from " + file)

    # for example: python3 py-ral-goog.py blankGoogleSheet --docid 1eB_amBkQKIU58ivzJ4Yyqefhc1XPWbTQ4BDtHdSJKbQ --tab Sheet1
    elif action.lower() == 'blankgooglesheet':
        g = google_connector.g(docid, tab)
        print ("Now blanking the Google Sheet")
        g.blankGoogleSheet()

    # for example: python3 py-ral-goog.py getNewRows --docid 1eB_amBkQKIU58ivzJ4Yyqefhc1XPWbTQ4BDtHdSJKbQ --tab Sheet1 --file file.csv
    elif action.lower() == 'getnewrows':
        g = google_connector.g(docid, tab)
        df_sheet = g.getGoogleSheet()
        df_file = pd.read_csv(file)
        data = g.getNewRows(df_sheet, df_file)
        print (data)

    else:
        print ("Error: That's not a valid command")

if __name__ == '__main__':
    run()