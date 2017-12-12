import csv
import json
import sys
import psycopg2

# Gets credentials for news database from JSON file
def getDBCredentials(jsonCreds):
	creds = json.load(jsonCreds)
	return creds

def connectDB(creds):
	host = creds["host"]
	username = creds["user"]
	password = creds["passwd"]
	dbName = creds["db"]
	db = psycopg2.connect(host=host, user=username, password=password, dbname=dbName)
	return db

def getCSVData(dataFile):
	try:
		data = open(dataFile)
		return data
	except:
		sys.stderr.write("Error: Invalid data file\n")
		sys.exit(1) 

# Loads article
def loadArticleFeatureData(articleData, db):
	cursor = db.cursor()
	# Creates table
	tableCreateSQL = open("sql/articleFeatures.sql").read()
	cursor.execute(tableCreateSQL)
	# Loads CSV data into table
	cursor.copy_from(articleData, "articleFeatures", sep=",")
	# Creates indices
	indexCreateSQL = open("sql/articleFeatures2.sql").read()
	cursor.execute(indexCreateSQL)

	db.commit()

def loadArticleMetadata(articleData, db):
	cursor = db.cursor()
	# Creates table
	tableCreateSQL = open("sql/articleMetadata.sql").read()
	cursor.execute(tableCreateSQL)
	# Loads CSV data into table
	cursor.copy_from(articleData, "articleMetadata", sep=",")

	db.commit()


def loadTopSourcePhrasesData(topSourcePhrasesData, db):
	cursor = db.cursor()
	# Creates table
	tableCreateSQL = open("sql/topSourcePhrases.sql").read()
	cursor.execute(tableCreateSQL)
	# Loads CSV data into table
	cursor.copy_from(topSourcePhrasesData, "topSourcePhrases", sep=",")

	db.commit()

def loadSourceMetadata(sourceMetadata, db):
	cursor = db.cursor()
	# Creates table
	tableCreateSQL = open("sql/sourceMetadata.sql").read()
	cursor.execute(tableCreateSQL)
	# Loads CSV data into table
	cursor.copy_from(sourceMetadata, "sourceMetadata", sep=",")

	db.commit()

if __name__ == "__main__":
	credsFile = "../../dbCredentials.json"

	# Check that credentials and article data files exist
	jsonCreds = ""
	try:
		jsonCreds = open(credsFile)
	except:
		sys.stderr.write("Error: Invalid database credentials file\n")
		sys.exit(1)

	creds = getDBCredentials(jsonCreds)
	db = connectDB(creds)

	articleFeatureData = getCSVData("data/articleFeatures.csv")
	loadArticleFeatureData(articleFeatureData, db)

	articleMetadata =  getCSVData("data/articleMetadata.csv")
	loadArticleMetadata(articleMetadata, db)
	
	topSourcePhrasesData = getCSVData("data/topSourcePhrases.csv")
	loadTopSourcePhrasesData(topSourcePhrasesData, db)

	sourceMetadata = getCSVData("data/sourceMetadata.csv")
	loadSourceMetadata(sourceMetadata, db)


	
