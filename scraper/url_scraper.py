import sys
from goose import Goose
import unicodedata
import tldextract

sys.setrecursionlimit(2500)

def fix(text):
    try:
        text = text.decode("ascii", "ignore")
    except:
        t=[unicodedata.normalize('NFKD', unicode(q)).encode('ascii','ignore') for q in text]
        text=''.join(t).strip()
    return text

def scrape(url):
    print "Starting Scraper"
    g = Goose()
    try:
        article = g.extract(url=url)
    except:
         return "Unexpected error when scraping", sys.exc_info()[0]
    text = fix(article.cleaned_text)
    title = fix(article.title)
    domain = tldextract.extract(url)[1]

    return title, text, domain
