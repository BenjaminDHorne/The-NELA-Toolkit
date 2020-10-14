# The News Landscape (NELA) Toolkit

**NOTE**: This code is for research purposes only! 

**NOTE**: The prediction models in this repository are outdated. Please do not make conclusions from the output of models. 

**NOTE**: This repository requires the LIWC 2007 Dictionary. To access the dictionary, please contact Dr. James Pennebaker: pennebaker@utexas.edu. The dictionary can be placed in the resources folder once aquired.

The News Landscape (NELA) Toolkit is built using Flask, Javascript, and PostgreSQL.

The project is currently being served using NGNIX and Gunicorn at **nelatoolkit.science**. 

Under “Check a News Article" users can provide a url to a news
article or manually enter news article text. The tool then performs
several predictions on the article: reliability, political impartiality,
title objectivity, text objectivity, and several online community
interest predictions. Each of these predictions is displayed as a
probability and each article with associated predictions are entered
into a table. As more article entries are provided, this table can be
sorted and filtered by different predictions using the table filters
menu at the top of the page. Further, more details about the article
and analysis of the article can be found by clicking on the entry
in the table. The ultimate goal of this page is to allow journalist
and information analyst to quickly filter articles down to ones that
need to be fact-checked or are of interest.

Under “Compare News Sources" users can explore and compare
a variety of news sources using content-based features. Specifically,
users can select multiple features, sources, and a time range to
visualize on a 2-dimensional scatter plot. For example, a user can
select “reading complexity" for the x-axis and “negative sentiment"
for the y-axis using the chart setting menu on the left side of the
page. They can then select any number of sources from our data set
and a data range over which to explore. The tool will then generate
a scatter plot of the selected sources for comparison. If a user wants
more details about a source, they can double-click the source bubble
in the scatter plot. This detailed page will show source metadata,
credibility predictions, and Facebook engagement over time. These
details can also be found on the “View All Sources" page.

## Using the toolkit locally

### PostgreSQL

To support the tool's back-end, [PostgreSQL](https://www.postgresql.org/) must be downloaded. In PostgreSQL, create a database with any name (e.g. NELA). You will need to create a database credentials JSON file named **dbCredentials.json** outside of the cloned directory (eg. ../dbCredentials.json). The format for the JSON file is shown below:

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

## Running The Tool with Flask

Here is a great guide to running flask locally: http://flask.pocoo.org/docs/0.12/quickstart/.

For NELA, running the app should look something like this:

	export FLASK_APP=app.py
	flask run
	Running on http://127.0.0.1:5000/

If you are running locally on Windows rather than Linux, use set instead of export:
	
	set FLASK_APP=app.py
	python -m flask run
	Running on http://127.0.0.1:5000/
	
	
## For Windows Users

If you are setting up the system on Windows, you will likely run into an issue with the pickled files (all files that end in .sav). Please check out inscructions in /pickle_converter to fix this.

## Project Data Details

The toolkit is divided into two main parts: Check a News Article and Compare News Sources.

### Check a News Article
#### classifiers/resources/

This folder contains the pre-trained machine learning models for predicting reliability, bias, subjectivity, and community interest. 

#### features/resources/

This folder contains all the needed lexicons, pre-trained models, and features selection lists for the feature computation and selection portion of the toolkit. 

### Compare News Sources
#### dbSetup/data.zip

This folder contains the data which is loaded into the tool's database. For each CSV, the data labels and types can be found by referring to its .sql file located under dbSetup/sql. 

**_articleFeatures.csv_**: Contains all computed features for each article in the dataset; it also includes the article's published date and its news source 

**_articleMetadata.csv_**: Contains the link and full title for each article within the dataset 

**_sourceMetadata.csv_**: Contains a credibility and impartiality score for each news source, along with a flag indicating if the source is self-identified as satire

**_topSourcePhrases.csv_**: Contains the top ten phrases for each news source, for every month (identified by a month number and year); sources that have more than 1 phrase but less than 10 for a given month will have a "NULL" field for phrases not contained

#### static/js/sourceData.js

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

#### static/js/featureData.js

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


## Usage

Copyright (c) 2017, Benjamin D. Horne and Sibel Adali
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

        • Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
        • Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
	
Any publication resulting from the use of this work must cite the following publication::

Benjamin D. Horne, William Dron, Sara Khedr, and Sibel Adali. "Assessing the News Landscape: A Multi-Module Toolkit for Evaluating the Credibility of News" WWW (2018).

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
	 






 

