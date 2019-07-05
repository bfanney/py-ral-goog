# py-ral-goog
The project will help you query Rally Kanban boards, create user stories, features, and tasks in Rally, and use a Google form to create Rally features. It includes two libraries, rally_connector.py and google_connector.py, which contain classes to help you connect and use both tools. The project also contains a command line interface, py-ral-goog.py, that relies on a YAML file, config.yaml, to connect to your Rally instance. You'll also need a JSON file of Google credentials to use the Google connector's capabilities.

I'll explain how to use the project from the command line below.

<h2>Rally capabilities</2>

<h3>Download all the user stories from a project and extract the metadata into a .csv file</h3>

<code>python3 py-ral-goog.py getBoard --fields MRM,RequestedBy</code>

Use the fields argument to write out a comma seperated listof metadata fields you need. Try fetching an individual feature (see the example below) to see all of the available metadata fields.

<h3>Download and display all the metadata associated with a feature or user story</h3>

<code>python3 py-ral-goog.py getFeature --f f12345</code>

<code>python3 py-ral-goog.py getUserStory --us US12345</code>

<h3>Create features and user stories</h3>

<code>python3 py-ral-goog.py setFeature --fields "{'Name':'Testing123', 'Description':'DeleteMe'}"</code>

<code>python3 py-ral-goog.py setUserStory --fields "{'Name':name,'PortfolioItem':'1234567891011','Description':'TextHere','Language':'ES','RequestedBy':'NameHere'}"</code>.

<h3>Get all of the tasks for a particular user story.</h3>

<code>py-ral-goog.py getTasks --us US12345</code>

<h3>Set a task for a particular user story</h3>

<code>python3 py-ral-goog.py setTask --fields "{'Name':'NameHere','WorkProduct':1234567891011}"</code>
  
<h2>Google Sheet capabilities</h2>

<h3>Download a Google Sheet as a CSV</h3>

<code>python3 py-ral-goog.py setGoogleSheet --docid 1eB_amBkQKIU58ivzJ4Yyqefhc1XPWbTQ4BDtHdSJKba --tab Sheet1 --file file.csv</code>

<h3>Compare a CSV file against a Google Sheet and identify new rows in the Google Sheet</h3>

<code>python3 py-ral-goog.py getNewRows --docid 1eB_amBkQKIU58ivzJ4Yyqefhc1XPWbTQ4BDtHdSJKba --tab Sheet1 --file file.csv</code>

<h3>Blank a Google Sheet</h3>

<code>python3 py-ral-goog.py blankGoogleSheet --docid 1eB_amBkQKIU58ivzJ4Yyqefhc1XPWbTQ4BDtHdSJKba --tab Sheet1</code>
