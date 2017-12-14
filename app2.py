#!/usr/bin/env python

import json
import sys
import os
import logging

from flask import Flask, request, render_template, url_for, send_from_directory, redirect
app = Flask(__name__)
app.logger.setLevel(logging.ERROR)

sys.path.append("..")
from credibility_toolkit import parse_url

@app.after_request
def add_header(response):
  """
  Add headers to both force latest IE rendering engine or Chrome Frame, and
  also to cache the rendered page for 10 minutes.
  """
  response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
  response.headers['Cache-Control'] = 'public, max-age=0'
  return response

@app.route('/js/<path:path>')
def send_js(path):
  """
  expose the js directory so we don't have to have everything in static
  """
  return send_from_directory('js', path)

@app.route("/")
def default():
  """
  default route
  """
  return render_template('view_all.html', json="static/output.json")

@app.route("/article", methods=['GET', 'POST'])
def article():
  """
  when the user wants to add an article, this function will get called. We will
  then load the json file, run the credibility toolkit on the url, and then
  append the results to the json file.
  """
  url = False
  if 'url' in request.form :
    url = request.form['url']

    with open(os.path.join("static", "output.json"), 'r') as infile:
      output = json.load(infile)

    # check if we already have this url parsed, if so, reparse it
    output["urls"] = filter(lambda x: x["url"] != url, output["urls"])

    parse_url(output, url)

    with open(os.path.join("static", "output.json"), 'w') as outfile:
      json.dump(output, outfile, indent=2)

  #return render_template('view_all.html', json="static/output.json", newurl=url)
  return redirect("/", code=302)

@app.route("/remove", methods=['GET', 'POST'])
def remove():
  """
  remove an article from output.json
  """
  url = False
  if 'url' in request.form :
    url = request.form['url']

    with open(os.path.join("static", "output.json"), 'r') as infile:
      output = json.load(infile)

    # check if we already have this url parsed, if so, reparse it
    output["urls"] = filter(lambda x: x["url"] != url, output["urls"])

    with open(os.path.join("static", "output.json"), 'w') as outfile:
      json.dump(output, outfile, indent=2)

  return redirect("/", code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
