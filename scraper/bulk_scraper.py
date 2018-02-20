import sys
import os
import urllib
import urllib2
import json
import feedparser
from bs4 import BeautifulSoup
import time
from dateutil import parser
from goose import Goose
import re
import pytz
import unicodedata
import io

g = Goose()

def fix(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')

def RSSfeed(source, url):
    news = []
    feed = feedparser.parse(url)

    for article in feed["entries"]:
        href = article["link"]
        # print href
        title = article["title"]

        request = urllib2.Request(href, headers={"User-Agent": "Magic-Browser"})
        response = urllib2.urlopen(request)
        if (response.code != 200):
            continue

        articleText = ""
        articleText = g.extract(url=href).cleaned_text

        news.append((fix(title), fix(articleText), source))
    return news


def sources():
    scraped_data = {}

    # New York Times
    key = "nytimes"
    name = "The New York Times"
    url = "http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml"
    scraped_data[key] = [name, RSSfeed(name, url), url]

    # Activist Post
    key = "activistpost"
    name = "Activist Post"
    url = "http://www.activistpost.com/feed"
    scraped_data[key] = [name, RSSfeed(name, url), url]

    # Russia Today
    key = "rt"
    name = "Russia Today"
    url = "https://www.rt.com/rss/usa/"
    scraped_data[key] = [name, RSSfeed(name, url), url]

    # Info Wars
    key = "infowars"
    name = "InfoWars"
    url = "https://www.infowars.com/category/us-news/feed/"
    scraped_data[key] = [name, RSSfeed(name, url), url]

    # End the Fed
    key = "endthefed"
    name = "End the Fed"
    url = "http://endthefed.org/feed/"
    scraped_data[key] = [name, RSSfeed(name, url), url]

    # Gateway Pundit
    key = "gatewaypundit"
    name = "The Gateway Pundit"
    url = "http://www.thegatewaypundit.com/feed/"
    scraped_data[key] = [name, RSSfeed(name, url), url]

    return scraped_data


def bulk_scraper():
    scraped_data = sources()
    return scraped_data
