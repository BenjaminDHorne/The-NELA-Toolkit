from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
import sys
import ast
from collections import OrderedDict

app = Flask(__name__)
db = SQLAlchemy()
monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

@app.route("/sourceComparator")
def main():
	return render_template('sourceComparator.html')

@app.route("/about")
def aboutPage():
	return render_template('about.html')

@app.route("/newsSource")
def sourcePage():
	return render_template('newsSource.html')

@app.route("/allSources")
def allSourcesPage():
	return render_template('allSources.html')

### --- Define internal APIs ---

### -- Internal APIs for news source page ---

@app.route("/getSourcePublishCounts")
def sendSourcePublishCounts():
	source = request.args.get("source")

	sqlStatement = 	"SELECT * " \
					"FROM sourcePublishCounts " \
				    "WHERE source = '%s' " \
				    "ORDER BY month" %(source)

	results = db.engine.execute(sqlStatement)

	data = OrderedDict()
	for row in results:
		month = monthNames[row[1]-1] 
		count = row[2]
		data[month] = count

	response = app.response_class(
		response = json.dumps(data),
		status = 200,
		mimetype='application/json'
	)

	return response

@app.route("/getSourceFacebookEngagement")
def sendSourceFacebookEngagement():
	source = request.args.get("source")

	sqlStatement = 	"SELECT * " \
					"FROM sourceFacebookEngagement " \
				    "WHERE source = '%s' " \
				    "ORDER BY month" %(source)

	results = db.engine.execute(sqlStatement)

	data = OrderedDict()
	for row in results:
		month = monthNames[row[1]-1] 
		comments = row[2]
		shares = row[3]
		reactions = row[4]
		data[month] = {}
		data[month]["comments"] = comments
		data[month]["shares"] = shares
		data[month]["reactions"] = reactions

	response = app.response_class(
		response = json.dumps(data),
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

	sqlStatement = 	"SELECT * " \
					"FROM topSourcePhrases " \
				    "WHERE source = '%s' and month = '%d' " %(source, month)

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
		print row
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


def formatCount(num):
	if num < 9999:
		return num
	else:
		newRepr = float(num/1000)
		newRepr = str(format(newRepr, '.1f')) + "k"
		return newRepr

if __name__ == "__main__":
	credsFile = "dbSetup/dbCredentials.json"
	jsonCreds = ""
	try:
		jsonCreds = open(credsFile)
	except:
		sys.stderr.write("Error: Invalid database credentials file\n")
		sys.exit(1)

	creds = json.load(jsonCreds)
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
	app.run(host='0.0.0.0', port=80, threaded=True)
