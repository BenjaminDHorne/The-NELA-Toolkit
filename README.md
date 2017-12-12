# The-Credibility-Toolkit

The Credibility Toolkit is a visual tool-set that provides several measures of assessing a news source's reliability. Currently, it uses 7 months of data, collected from 92 distinct news sources. 

The Credibility Toolkit was built using the Flask framework and uses PostgreSQL as its database. 

The project is currently running at **http://104.236.229.25/**. 

## Installing Dependencies

### PostgreSQL

To support the tool's back-end, [PostgreSQL](https://www.postgresql.org/) must be downloaded. In PostgreSQL, create a database with any name (e.g. NELA). You will need to create a database credentials JSON file named **dbCredentials.json** outside of the cloned directory. The format for the JSON file is shown below:

    {
    	"host":"",
    	"user":"",
    	"passwd":"",
    	"db":"",
    	"port":""
    }

### Python Dependencies

To run the tool, [Python 2.7](https://www.python.org/downloads/) must be downloaded.  

The easiest way to download all necessary Python packages is using [pip](https://pypi.python.org/pypi/pip). To do so, navigate to the project root directory and run:

	pip install -r requirements.txt

## Loading Data

To load the data into the newly created PostgreSQL database, navigate to the /dbSetup directory in the project directory. Extract the contents of the data.zip folder in the /dbSetup directory. Then, run:

	python load.py

## Running The Tool

Within the root project directory, run:
	
	python app.py

The project is configured with a host of 0.0.0.0 and port 80.

## Project Data Details

### dbSetup/data.zip

This folder contains the data which is loaded into the tool's database. For each CSV, the data labels and types can be found by referring to its .sql file located under dbSetup/sql. 

**_articleFeatures.csv_**: Contains all computed features for each article in the dataset; it also includes the article's published date and its news source 

**_articleMetadata.csv_**: Contains the link and full title for each article within the dataset 

**_sourceMetadata.csv_**: Contains a credibility and impartiality score for each news source, along with a flag indicating if the source is self-identified as satire

**_topSourcePhrases.csv_**: Contains the top ten phrases for each news source, for every month (identified by a month number and year); sources that have more than 1 phrase but less than 10 for a given month will have a "NULL" field for phrases not contained

### badCollection.json

This file located in the project's root directory contains information on issues with the collection for certain news sources. It provides a way to display this issue on the tool. 

For the example shown below, there were issues collecting Drudge Report for May 2017. This means that there are zero articles for the Drudge Report for May 2017 due to issues with the way it was collected **NOT** because the source didn't publish that month.

	{
		"Drudge Report":
		[
			{
				"month": 5,
				"year": 2017
			}
		]
	} 


### static/js/sourceData.js

Additional news source metadata is stored here (e.g. source's display name, date founded, etc). Each news source has an associated image, which is located in the /static/newsSourceImages directory.

A portion of this data is shown below for the source AP:

	"AP":
	{
		"name": "Associated Press (AP)",
		"type": "Radio, television, and online",
		"country": "United States",
		"founded": "May 22, 1846",
		"website": "ap.org",
		"imageName": "AP.jpg"
	}

### static/js/featureData.js

The mapping between each of the article's computed features and its display name on the tool is stored here. Each name aims to be concise, while providing more information on the nature of the feature.

This file also stores the top ten features, which are the initial options in the tool-set.

A portion of this data is shown below:

	{
	...
	    "Average Word Length": "wordlen",
        "Word Count": "WC",
        "Probability of Objectivity": "NB_pobj",
        "Probability of Subjectivity": "NB_psubj",
        "Quote Usage": "quotes",
	...
	}


 


	 






 

