#!/usr/bin/env python

from flask import Flask, render_template, request, url_for, send_from_directory, redirect, session
from flask_sqlalchemy import SQLAlchemy
import json
import sys
import ast
from collections import OrderedDict
import datetime 
import os
import logging
import uuid
import glob
import shutil
from credibility_toolkit import parse_url, parse_text
import platform

app = Flask(__name__)
monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
badCollectionData = {}


##### main stuf that needs to be outside the main when served by gunicorn and nginx. main is not ran unless called with python
credsFile = "../dbCredentials.json"
jsonCreds = ""
try:
	jsonCreds = open(credsFile)
except:
	sys.stderr.write("Error: Invalid database credentials file\n")
	sys.exit(1)

creds = json.load(jsonCreds)

bcd = open("badCollection.json")
badCollectionData = json.load(bcd)

POSTGRES = {
	'user': creds["user"],
	'pw': creds["passwd"],
	'db': creds["db"],
	'host': creds["host"],
	'port': creds["port"]
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db = SQLAlchemy(app)
db.session.commit()

for tmp in glob.glob(os.path.join("static", "tmp-*")):
	try:
		os.remove(tmp)
	except:
		pass

app.secret_key = str(uuid.uuid4())
####################################################

@app.after_request
def add_header(response):
  """
  Add headers to both force latest IE rendering engine or Chrome Frame, and
  also to cache the rendered page for 10 minutes.
  """
  response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
  response.headers['Cache-Control'] = 'public, max-age=0'
  return response

@app.route("/")
def home():
	return render_template('home.html')

@app.route("/credibilitytoolkit")
def credibility():
  if 'tmpfile' not in session or not os.path.isfile(session['tmpfile']):
      session['tmpfile'] = os.path.join("static", "tmp-" + str(uuid.uuid4()))
      if platform.system() == "Windows":
	session['tmpfile'] = session['tmpfile'].replace("\\", "/")
      shutil.copy2(os.path.join("static", "output.json"), session['tmpfile'])

  return render_template('credibility.html', json=session['tmpfile'])

@app.route("/visualizationtoolkit")
def main():
	return render_template('sourceComparator.html')

@app.route("/about")
def aboutPage():
	return render_template('about.html')
	
@app.route("/datasetRequest")
def dataPage():
	return render_template('datasetRequest.html')

@app.route("/help")
def help():
	return render_template('help.html')

@app.route("/newssource")
def sourcePage():
	return render_template('newsSource.html')

@app.route("/allsources")
def allSourcesPage():
	return render_template('allSources.html')

@app.route("/features")
def features():
	return render_template('features.html')

# --- Credibility toolkit internal APIs

def send_error(text):
    return """
    <html><body><script>
    alert("%s");
    location.replace("%s");
    </script></body></html>
    """ % (text, url_for('credibility'))

@app.route("/article", methods=['GET', 'POST'])
def article():
  """
  when the user wants to add an article, this function will get called. We will
  then load the json file, run the credibility toolkit on the url, and then
  append the results to the json file.
  """
  if 'tmpfile' not in session or not os.path.isfile(session['tmpfile']):
      return 'ERROR: Unable to find JSON file'

  if 'url' not in request.form :
      return 'ERROR: No URL in POST'

  url = request.form['url']

  with open(session['tmpfile'], 'r') as infile:
    output = json.load(infile)

  # check if we already have this url parsed, if so, reparse it
  output["urls"] = filter(lambda x: x["url"] != url, output["urls"])

  try:
    parse_url(output, url)

    with open(session['tmpfile'], 'w') as outfile:
        json.dump(output, outfile, indent=2)

  except Exception as inst:
      return send_error(inst)

  return redirect(url_for('credibility'), code=302)

@app.route("/clear")
def clear():
  if 'tmpfile' in session:
    tmp = session.pop('tmpfile')
    try:
      os.remove(tmp)
    except:
      pass

  session['tmpfile'] = os.path.join("static", "tmp-" + str(uuid.uuid4()))
  if platform.system() == "Windows":
      session['tmpfile'] = session['tmpfile'].replace("\\", "/")
  with open(session['tmpfile'], 'w') as outfile:
      output = {'urls':[]}
      json.dump(output, outfile, indent=2)

  return redirect(url_for('credibility'), code=302)

@app.route("/reset")
def reset():
  if 'tmpfile' in session:
    tmp = session.pop('tmpfile')
    try:
      os.remove(tmp)
    except:
      pass
  return redirect(url_for('credibility'), code=302)

@app.route("/manual", methods=['GET', 'POST'])
def manual():
  """
  when the user wants to add an article, this function will get called. We will
  then load the json file, run the credibility toolkit on the url, and then
  append the results to the json file.
  """
  if 'tmpfile' not in session or not os.path.isfile(session['tmpfile']):
    return send_error('ERROR: Unable to find JSON file')

  if 'manual_entry_title' not in request.form :
    return send_error('ERROR: Empty Title')

  if 'manual_entry_text' not in request.form :
    return send_error('ERROR: Empty Text')

  title = request.form['manual_entry_title']
  text = request.form['manual_entry_text']

  with open(session['tmpfile'], 'r') as infile:
    output = json.load(infile)

  try:
    parse_text(output, title, text)

    with open(session['tmpfile'], 'w') as outfile:
        json.dump(output, outfile, indent=2)

  except Exception as inst:
      return send_error(inst)

  return redirect(url_for('credibility'), code=302)

@app.route("/remove", methods=['GET', 'POST'])
def remove():
  """
  remove an article from output.json
  """
  if 'tmpfile' not in session or not os.path.isfile(session['tmpfile']):
    return send_error('ERROR: Unable to find JSON file')

  url = request.form['url']

  if len(url) > 3:
    with open(session['tmpfile'], 'r') as infile:
      output = json.load(infile)

    # check if we already have this url parsed, if so, reparse it
    output["urls"] = filter(lambda x: x["url"] != url, output["urls"])

    with open(session['tmpfile'], 'w') as outfile:
      json.dump(output, outfile, indent=2)

  return redirect(url_for('credibility'), code=302)

### --- Define internal APIs ---

### -- Internal APIs for news source page ---

@app.route("/getSourceMetadata")
def sendSourceMetadata():
	source = request.args.get("source")

	# Gets latest computed values
	sqlStatement = "SELECT * " \
				   "FROM sourceMetadata " \
				   "WHERE source = '%s' " \
				   "ORDER BY dateComputed " \
				   "LIMIT 1 " %(source)

	results = db.engine.execute(sqlStatement)
	data = {}
	for row in results:
		data["perCredible"] = '{0:.3g}'.format(row[1]*100)
		data["perImpartial"] = '{0:.3g}'.format(row[2]*100)
		data["isSatire"] = row[3]

		print row

	response = app.response_class(
		response = json.dumps(data),
		status = 200,
		mimetype='application/json'
	)

	return response

# Gets valid month + year for which source has published articles
@app.route("/getSourcePublishDates")
def sendValidSourcePublishDates():
	source = request.args.get("source")
	times = getSourcePublishDates(source)
	data = {}
	data["dates"] = []
	for t in times:
		data["dates"].append(t.strftime("%b %Y"))

	response = app.response_class(
		response = json.dumps(data),
		status = 200,
		mimetype='application/json'
	)

	return response

def getSourcePublishDates(source):
	sqlStatement = "SELECT make_date(CAST(y AS INTEGER), CAST(m AS INTEGER), 1) " \
					   "FROM" \
					   	"( " \
	  				   		"SELECT EXTRACT(YEAR FROM datePublished) as y, EXTRACT(MONTH FROM datePublished) as m " \
	  						"FROM articleFeatures " 
	if (source != ""):
		sqlStatement += "WHERE source = '%s' " %(source)


	sqlStatement += "GROUP BY EXTRACT(YEAR FROM datePublished), EXTRACT(MONTH FROM datePublished) " \
	  					") as findDates" 


	results = db.engine.execute(sqlStatement)
	times = []
	for row in results:
		times.append(row[0])

	print times
	times.sort()
	return times


@app.route("/getSourcePublishCounts")
def sendSourcePublishCounts():
	source = request.args.get("source")

	allDates = getSourcePublishDates("")

	sqlStatement = 	"SELECT EXTRACT(MONTH FROM datePublished) as m, EXTRACT(YEAR FROM datePublished) as y, COUNT(id) " \
					"FROM articleFeatures " \
				    "WHERE source = '%s' " \
				    "GROUP BY source, m, y" %(source)

	results = db.engine.execute(sqlStatement)

	data = {}
	for row in results:
		month = int(row[0])
		year = int(row[1])
		date = datetime.datetime(year, month, 1).strftime("%b %Y")
		count = row[2]
		data[date] = count

	dataSorted = OrderedDict()
	# Add 0 counts for months not available for source and asterix next to month name if due to bad collection
	for d in allDates:
		date = d.strftime("%b %Y")
		month = d.month
		year = d.year
		if date not in data:
			if (source in badCollectionData):
				for x in badCollectionData[source]:
					if x["month"] == month and x["year"] == year:
						date = "*" + date
						continue
			dataSorted[date] = {}
			dataSorted[date] = 0
		else:
			dataSorted[date] = data[date]

	response = app.response_class(
		response = json.dumps(dataSorted),
		status = 200,
		mimetype='application/json'
	)

	return response

@app.route("/getSourceFacebookEngagement")
def sendSourceFacebookEngagement():
	source = request.args.get("source")

	allDates = dates = getSourcePublishDates("")

	sqlStatement = 	"SELECT EXTRACT(MONTH FROM datePublished) as m, EXTRACT(YEAR FROM datePublished) as y, SUM(FB_Comment_Counts), SUM(FB_Share_Counts), SUM(FB_Reaction_Counts ) " \
					"FROM articleFeatures " \
				    "WHERE source = '%s'" \
				    "GROUP BY source, m, y" %(source)

	results = db.engine.execute(sqlStatement)

	data = {}
	for row in results:
		month = int(row[0])
		year = int(row[1])
		date = datetime.datetime(year, month, 1).strftime("%b %Y")
		comments = row[2]
		shares = row[3]
		reactions = row[4]
		data[date] = {}
		data[date]["comments"] = comments
		data[date]["shares"] = shares
		data[date]["reactions"] = reactions

	dataSorted = OrderedDict()
	# Add 0 counts for months not available for source
	for d in allDates:
		date = d.strftime("%b %Y")
		if date not in data:
			dataSorted[date] = {}
			dataSorted[date]["comments"] = 0
			dataSorted[date]["shares"] = 0
			dataSorted[date]["reactions"] = 0
		else:
			dataSorted[date] = data[date]


	response = app.response_class(
		response = json.dumps(dataSorted),
		status = 200,
		mimetype='application/json'
	)

	return response

@app.route("/getMostSharedArticles")
def sendMostSharedArticles():
	source = request.args.get("source")

	sqlStatement = 	"SELECT articleMetadata.url, articleMetadata.title, articleFeatures.FB_Share_Counts " \
					"FROM articleMetadata " \
					"INNER JOIN articleFeatures ON articleMetadata.id = articleFeatures.id " \
				    "WHERE articleFeatures.source = '%s' " \
				    "ORDER BY articleFeatures.FB_Share_Counts DESC " \
				    "LIMIT 10" %(source)

	results = db.engine.execute(sqlStatement)

	data = {}
	data["articles"] = []
	for row in results:
		url = row[0]
		title = row[1]
		shares = row[2]
		articleData = {}
		articleData["url"] = url
		articleData["title"] = title
		articleData["shares"] = shares
		data["articles"].append(articleData)
	
	response = app.response_class(
		response = json.dumps(data),
		status = 200,
		mimetype='application/json'
	)

	return response

@app.route("/getTopSourcePhrases")
def sendTopPhrases():
	source = request.args.get("source")
	month = int(request.args.get("month"))
	year = int(request.args.get("year"))

	sqlStatement = 	"SELECT * " \
					"FROM topSourcePhrases " \
				    "WHERE source = '%s' and month = '%d' and year = '%d' " %(source, month, year)

	results = db.engine.execute(sqlStatement)

	data = {}
	data["orderedPhrases"] = []
	for row in results:
		# Gets the top 5 phrases, ignoring any NULL ones
		for i in range(2, 7):
			phrase = row[i]
			if (phrase != "NULL"):
				data["orderedPhrases"].append(phrase)

	
	response = app.response_class(
		response = json.dumps(data),
		status = 200,
		mimetype='application/json'
	)

	return response

## -- Internal APIs for bubble chart page ---

@app.route("/getBubbleChartData") 
def sendBubbleChartData():
	sourceValue = request.args.get("sourceValue")
	xAxis = request.args.get("xAxis")
	yAxis = request.args.get("yAxis")
	bubbleColor = request.args.get("bubbleColor")
	bubbleSize = request.args.get("bubbleSize")
	startDate = request.args.get("startDate")
	endDate = request.args.get("endDate")
	selectedSources = ast.literal_eval(request.args.get('sources'))
	selectedSources = [s.strip() for s in selectedSources]
	selectedSources = ["'{0}'".format(s) for s in selectedSources]
	sqlStatement = ""

	if (sourceValue == "Median"):

		sqlStatement = "SELECT source, median(%s) as median_value, median(%s) as median_value, median(%s) as median_value, median(%s) as median_value, " %(xAxis, yAxis, bubbleColor, bubbleSize)
	
	elif (sourceValue == "Average"):

		sqlStatement = "SELECT source, AVG(%s), AVG(%s), AVG(%s), AVG(%s), " %(xAxis, yAxis, bubbleColor, bubbleSize)

	elif (sourceValue == "Maximum"):

		sqlStatement = "SELECT source, MAX(%s), MAX(%s), MAX(%s), MAX(%s), " %(xAxis, yAxis, bubbleColor, bubbleSize)

	sqlStatement += "COUNT('id'), MAX(FB_Share_Counts), MAX(FB_Comment_Counts), MAX(FB_Reaction_Counts) " \
					"FROM articleFeatures " \
				    "WHERE datePublished::date >= '%s' and datePublished::date <= '%s' and source in (%s)" \
				    "GROUP BY source" %(startDate, endDate, ", ".join(selectedSources))

	results = db.engine.execute(sqlStatement)

	data = {}
	data["values"] = []
	numArticles = 0
	numSources = 0
	mostFBShares = 0
	mostFBComments = 0
	mostFBReactions = 0

	for row in results:
		print str([row[0].encode('utf-8')] + list(row[1:5])) + ","
		if (mostFBShares < row[6]):
			mostFBShares = row[6]
		if (mostFBComments < row[7]):
			mostFBComments = row[7]
		if (mostFBReactions < row[8]):
			mostFBReactions = row[8]

		numSources += 1
		numArticles += row[5]

		sourceData = {}
		sourceData["source"] = row[0]
		sourceData["xAxis"] = row[1] * 1000
		sourceData["yAxis"] = row[2] * 1000
		sourceData["bubbleColor"] = row[3] * 1000
		sourceData["bubbleSize"] = row[4] * 1000
		data["values"].append(sourceData)

	data["numArticles"] = formatCount(numArticles)
	data["numSources"] = numSources
	data["mostFBShares"] = formatCount(mostFBShares)
	data["mostFBComments"] = formatCount(mostFBComments)
	data["mostFBReactions"] = formatCount(mostFBReactions)

	response = app.response_class(
		response = json.dumps(data),
		status = 200,
		mimetype='application/json'
	)

	return response 

@app.route("/getDateRange")
def sendDateRange():
	sqlStatement = "SELECT MIN(datePublished), MAX(datePublished) " \
				   "FROM articleFeatures" 

	results = db.engine.execute(sqlStatement)
	data = {}
	for row in results:
		data["startDate"] = row[0].strftime("%Y-%m-%d")
		data["endDate"] = row[1].strftime("%Y-%m-%d")


	response = app.response_class(
		response = json.dumps(data),
		status = 200,
		mimetype='application/json'
	)

	return response 

@app.route("/getAllSources")
def sendAllSources():
	sqlStatement = "SELECT DISTINCT(source) " \
				   "FROM articleFeatures"

	results = db.engine.execute(sqlStatement)
	data = {}
	data["sources"] = []
	for row in results:
		data["sources"].append(row[0])
	data["sources"].sort()

	response = app.response_class(
		response = json.dumps(data),
		status = 200,
		mimetype='application/json'
	)

	return response 


def formatCount(num):
	if num < 9999:
		return num
	else:
		newRepr = float(num/1000)
		newRepr = str(format(newRepr, '.1f')) + "k"
		return newRepr

@app.route('/js/<path:path>')
def send_js(path):
  """
  expose the js directory so we don't have to have everything in static
  """
  return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
  """
  expose the css directory so we don't have to have everything in static
  """
  return send_from_directory('static/css', path)

if __name__ == "__main__":
	credsFile = "../dbCredentials.json"
	jsonCreds = ""
	try:
		jsonCreds = open(credsFile)
	except:
		sys.stderr.write("Error: Invalid database credentials file\n")
		sys.exit(1)

	creds = json.load(jsonCreds)

	badCollectionData = open("badCollection.json")
	badCollectionData = json.load(badCollectionData)

	POSTGRES = {
		'user': creds["user"],
		'pw': creds["passwd"],
		'db': creds["db"],
		'host': creds["host"],
		'port': creds["port"]
	}

	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['DEBUG'] = True
	db = SQLAlchemy(app)
	db.session.commit()

	for tmp in glob.glob(os.path.join("static", "tmp-*")):
		try:
			os.remove(tmp)
		except:
			pass

	app.secret_key = str('2e239029-814f-4ece-b99c-1f539509ca10')
 
	app.run(host='0.0.0.0', port=80, threaded=True)
