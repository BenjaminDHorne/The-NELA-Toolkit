#!/usr/bin/env python

import sys
import os
import re
import uuid
import time
from threading import Thread, Lock

import features.Compute_all_features as Compute_all_features
import features.feature_selector as feature_selector

import classifiers.fake_filter as fake_filter
import classifiers.bias_filter as bias_filter
import classifiers.community_filter as community_filter
import classifiers.subjectivity_classifier as subjectivity_classifier
import scraper.url_scraper as scrape
import scraper.bulk_scraper as bulk_scraper

#from screenshot import get_screenshot
from collections import OrderedDict
import json

basepath = os.path.dirname(os.path.realpath(__file__))
featurepath = os.path.join(basepath, "out")


urls = [
  "http://mondoweiss.net/2017/10/businesses-hurricane-boycott/",
  "http://www.chron.com/neighborhood/bayarea/news/article/Dickinson-claims-no-Hurricane-Harvey-relief-if-12292001.php",
  "http://www.miamiherald.com/news/weather/hurricane/article175955031.html",
  "https://www.greenleft.org.au/content/imf-refuses-barbuda-debt-relief-after-hurricane-devastation-cuba-dispatches-medical-staff",
  "http://www.wsws.org/en/articles/2017/09/12/chem-s12.html",
  "https://theintercept.com/2017/10/19/to-get-hurricane-rebuilding-money-in-texas-contractors-must-promise-they-wont-boycott-israel/",
  "http://www.dailywire.com/news/22431/video-shows-where-puerto-ricos-aid-went-spoiler-chase-stephens#exit-modal",
  "http://www.miaminewtimes.com/news/miami-frustrated-with-fpl-after-hurricane-irma-9666311",
  "http://www.zerohedge.com/news/2017-09-02/red-cross-admits-it-doesnt-know-how-hurricane-harvey-donation-money-spent",
  "https://www.bloomberg.com/news/articles/2017-09-05/fema-is-almost-out-of-money-as-hurricane-irma-threatens-florida",
  "https://www.intellihub.com/gas-shortage-plagues-texas-cities-as-stations-run-out/",
  "https://www.intellihub.com/700b-unpaid-mortgage-balances-in-harvey-and-irma-disaster-areas/",
  "http://www.nydailynews.com/new-york/malliotakis-nyc-puerto-ricans-article-1.3572242",
  "https://www.democracynow.org/2017/10/18/rosa_clemente_on_puerto_ricans_drinking",
  "https://socialistaction.org/2017/10/17/rebuilding-puerto-rico-after-the-hurricane-all-wall-street-cares-about-is-their-money/",
  "https://amp.cnn.com/cnn/2017/10/13/politics/puerto-rico-recovery-poll/index.html",
  "http://www.bostonglobe.com/news/nation/2017/10/06/fema-removes-statistics-about-water-and-electricity-puerto-rico-from-its-website/Dq4HN1f0s7MSYi0iE7x30N/story.html?event=event25",
  "https://qz.com/1114413/hurricane-maria-puerto-ricans-washing-in-contaminated-water-face-the-spread-of-leptospirosis/",
  "http://thehill.com/homenews/senate/356295-sanders-to-visit-puerto-rico-instead-of-womens-convention#",
  "http://nypost.com/2017/10/19/stuck-without-power-puerto-rican-studio-dances-on/",
  "https://www.washingtonpost.com/news/food/wp/2017/10/18/post-maria-jose-andres-and-his-team-have-served-more-meals-in-puerto-rico-than-the-red-cross/?utm_term=.854d0ca7a2ec",
  "http://www.npr.org/2017/10/19/558375945/2-strangers-a-6-page-list-and-a-plan-hatched-to-help-puerto-rico?sc=tw",
  "https://www.usatoday.com/story/news/world/2017/10/18/real-death-toll-puerto-rico-probably-450-much-higher-than-official-count/774918001/",
  "https://barricades.news/volunteer-disaster-responders-fundraise-for-puerto-rico/",
  "https://www.dailykos.com/stories/2017/10/20/1708359/-FEMA-has-yet-to-authorize-full-disaster-help-for-Puerto-Rico-Island-Is-Test-bed-for-Drone-Deliveries#comment_68087711",
  "https://www.nytimes.com/2017/10/19/us/puerto-rico-electricity-power.html",
  "http://www.wsws.org/en/articles/2017/10/20/puer-o20.html",
  "http://www.fox9.com/news/heartfelt-reunion-mn-family",
  "https://www.outbreakobservatory.org/outbreakthursday-1/10/19/2017/the-growing-risk-of-leptospirosis-in-puerto-rico",
  "http://www.mcclatchydc.com/news/politics-government/congress/article179723621.html",
  "http://thehill.com/homenews/administration/357473-whitefish-energy-contract-bars-government-from-auditing-deal#.WfNuVFgmcQc.twitter",
  "https://shareblue.com/shady-contractor-from-trump-cronys-hometown-threatens-to-cut-off-puerto-rico-relief/",
  "http://thehill.com/homenews/news/357215-puerto-rico-governor-requests-audit-into-contract-awarded-to-tiny-energy#.WfL-RTb2o-I.twitter",
  "https://www.dailykos.com/stories/2017/10/30/1710970/-Critically-ill-Puerto-Rican-children-pay-the-price-for-incompetent-disaster-planning-and-response",
  "https://www.huffingtonpost.com/entry/puerto-rico-power-whitefish-contract-zinke_us_59f60718e4b03cd20b823156?ncid=engmodushpmg00000004",
  "https://paper.li/anitabondi/interplay?edition_id=304ae420-b5d7-11e7-b435-0cc47a0d15fd#/",
  "https://www.huffingtonpost.com/entry/leptospirosis-outbreak-puerto-rico-hurrincane_us_59e905aae4b0f9d35bc969ac?ncid=APPLENEWS00001",
  "http://mtpr.org/post/whitefish-company-wins-power-restoration-contract-puerto-rico",
  "http://www.cnn.com/2017/10/20/us/puerto-rico-one-month-santiago/index.html",
  "https://www.artsy.net/article/artsy-editorial-lin-manuel-miranda-joins-warhol-rauschenberg-foundations-hurricane-maria-relief-effort",
  "http://www.cnn.com/2017/10/19/us/puerto-rico-superfund-water-tests-safe-invs/index.html",
  "http://businessjournaldaily.com/fnb-donates-25k-to-victims-of-las-vegas-puerto-rico/?utm_content=61989263&utm_medium=social&utm_source=twitter",
  "https://www.ecowatch.com/food-water-crisis-puerto-rico-2498944175.html",
  "http://www.independent.co.uk/news/world/americas/trump-deportations-houston-harvey-hurricane-resume-after-pause-a7960381.html",
  "http://allnews4us.com/politics/breaking-texas-mosque-refuses-help-refugees-allah-forbids-helping-infidels",
  "http://www.independent.co.uk/news/world/americas/texas-faith-survivors-rescue-storm-flooding-victims-a7925331.html",
  "https://archive.is/p419m#selection-253.0-253.79",
  "https://www.cnbc.com/2017/10/29/puerto-rico-to-lean-on-ny-fl-for-help-restoring-its-grid-after-whitefish.html",
  "https://www.nbcnews.com/storyline/puerto-rico-crisis/puerto-rico-governor-calls-whitefish-energy-contact-bee-canceled-immediately-n815396",
  "https://theconservativetreehouse.com/2017/09/30/puerto-rico-teamsters-union-frente-amplio-refuse-to-deliver-supplies-use-hurricane-maria-as-contract-leverage/",
  "http://www.thegatewaypundit.com/2017/09/smoking-gun-san-juan-teamsters-didnt-show-work-distribute-relief-supplies-us-aid-rotting-ports/",
  "http://anews-24.com/2017/10/15/san-juan-city-council-votes-unanimously-to-impeach-trump-hating-mayor/",
  "https://web.archive.org/web/20170924173802/http://ourlandofthefree.com/2017/09/harvey-flooding-uncovers-secret-stash-of-ammo-hidden-by-obama-administration/",
  "https://www.vox.com/policy-and-politics/2017/10/25/16504870/puerto-rico-running-water",
  "http://www.npr.org/sections/thetwo-way/2017/10/25/560045944/tesla-turns-power-back-on-at-childrens-hospital-in-puerto-rico",
  "https://www.thenation.com/article/meet-the-legal-theorists-behind-the-financial-takeover-of-puerto-rico/",
  "http://yournewswire.com/las-vedas-eyewitness-false-flag/",
  "http://news.sky.com/story/las-vegas-shooting-crowd-warned-youre-all-going-to-die-11064484",
  "http://www.express.co.uk/news/uk/807982/Manchester-Arena-Ariana-Grande-terror-bomb-fears-explosion-Gunman-Oldham-Hospital?utm_content=bufferee23e&utm_medium=social&utm_source=twitter.com&utm_campaign=buffer",
  "https://www.dailystar.co.uk/news/latest-news/616507/manchester-men-arena-explosion-Oldham-hospital-closed-gun-armed-man-ariana-grande",
  "https://www.dailystar.co.uk/news/latest-news/656346/new-caledonia-tsunami-earthquake-7-magnitude-warning-pacific",
  "https://www.dailystar.co.uk/news/world-news/656226/north-korea-news-latest-60-minutes-sean-larkin-us-military-trump",
  "http://archive.is/55UVg",
  "http://www.dailymail.co.uk/news/article-4781878/North-Korea-nuclear-nerves-wipe-1-trillion-world-stocks.html",
  "https://www.egypttoday.com/Article/3/16761/North-Korea-nuclear-nerves-wipe-1-trillion-off-world-stocks",
  "https://www.adn.com/nation-world/2017/08/11/nuclear-nerves-wipe-1-trillion-off-world-stocks/",
  "https://nworeport.me/2017/08/13/nuclear-nerves-wipe-1-trillion-off-world-stocks/",
  "https://www.infowars.com/nuclear-nerves-wipe-1-trillion-off-world-stocks/",
  "https://www.infowars.com/buchanan-is-war-with-iran-now-inevitable-2/",
  "https://www.nytimes.com/2017/10/25/us/politics/alexander-murray-congressional-budget-office-deficit-savings.html?rref=collection%2Fsectioncollection%2Fpolitics&action=click&contentCollection=politics&region=stream&module=stream_unit&version=latest&contentPlacement=2&pgtype=sectionfront"
]

lock = Lock()

def add_classifier(info, name, func, *args):
  result = func(*args)

  lock.acquire()

  if "classifiers" not in info:
    info["classifiers"] = []
    info["cindex"] = OrderedDict()

  info["cindex"][name] = len(info["classifiers"])

  info["classifiers"].append({
    "name":name,
    "result":result
  })

  lock.release()

def parse_url(output, url):
  info = OrderedDict()
  info["url"] = url

  if url:
    try:
      info["title"], info["text"], info["source"] = scrape.scrape(url)
    except:
      print "WARNING: Unable to scrape:", url
      return

  else:
    info["text"] = "FAKE FAKE FAKE Clinton is terrible Mainstream media sucks. The real patriots can see this FRAUD!"
    info["title"] = "BREAKING Fraudulent Clinton Votes Discovered By The Tens Of Thousands, wait until you see this! Those dems are at it again."
    info["source"] = "unknown"

  # Try to get the thumbnail
  #fname = re.sub("[^0-9a-z_]", "", info["title"].replace(" ", "_").lower()[:50]) + ".png"
  #fname = info["source"] + "_" + fname
  #path = os.path.join("web", "static", fname)
  #try:
  #  #if not os.path.isfile(path):
  #  #  get_screenshot(path, url)
  #  info["screenshot"] = os.path.join("static", fname)
  #except:
  #  pass

  parse_info(output, info)

def parse_text(output, title, text):
  info = OrderedDict()
  info["url"] = str(uuid.uuid4())
  info["source"] = "unknown"

  info["title"] = title
  info["text"] = text

  parse_info(output, info)

def parse_info(output, info):
  info["title"] = info["title"].strip()
  info["text"] = info["text"].strip()
  info["source"] = info["source"].strip()

  if not info["title"] or not info["text"]:
    raise ValueError("WARNING: Unable to parse: ", info["url"])
    return

  if len(info["text"]) < 100:
    raise ValueError("WARNING: URL text too short: ", info["url"])
    return

  print
  print info["url"]
  print info["title"]
  print info["source"]

  start_time = time.time()

  #feature creation and selection
  Compute_all_features.start(info["title"], info["text"], info["source"], featurepath)
  feature_selector.feature_select(featurepath)

  #classifiers

  if True: # Set to true for threading, false otherwise
    threads = []
    threads.append(Thread(target=add_classifier, args=(info, "fake_filter", fake_filter.fake_fitler, featurepath,)))
    threads.append(Thread(target=add_classifier, args=(info, "bias_filter", bias_filter.bias_fitler, featurepath,)))
    threads.append(Thread(target=add_classifier, args=(info, "community_filter", community_filter.community_fitler, featurepath,)))
    threads.append(Thread(target=add_classifier, args=(info, "subjectivity_classifier", subjectivity_classifier.subjectivity, info["title"], info["text"],)))

    for t in threads:
      t.daemon = True
      t.start()

    for t in threads:
      t.join()

  else:
    add_classifier(info, "fake_filter", fake_filter.fake_fitler, featurepath)
    add_classifier(info, "bias_filter", bias_filter.bias_fitler, featurepath)
    add_classifier(info, "community_filter", community_filter.community_fitler, featurepath)
    add_classifier(info, "subjectivity_classifier", subjectivity_classifier.subjectivity, info["title"], info["text"])

  for val in info["classifiers"]:
    print val["name"], ":", val["result"]

  print "Parsing took %.4f seconds" % (time.time() - start_time)
  print

  output["urls"].append(info)

def source_test():
  source_result_dict = {}
  data = bulk_scraper.bulk_scraper()
  for key in data.keys():
    fake_source_results = []
    bias_source_results = []
    for source, article, url in data[key]:
      try:
        Compute_all_features.start(article[0], article[1], article[2], featurepath)
      except ValueError:
        continue
      feature_selector.feature_select(featurepath)
      f = fake_filter.fake_fitler(featurepath)
      b = bias_filter.bias_fitler(featurepath)
      fake_source_results.append(f[0][0])
      bias_source_results.append(b[0][0])
    reliable_arts = [1 for r in fake_source_results if r == 'Credibile Writing Style']
    unbiased_arts = [1 for r in bias_source_results if r == 'UnBiased Writing Style']
    per_reliable = float(sum(reliable_arts)) / len(fake_source_results)
    per_unbiased = float(sum(unbiased_arts)) / len(bias_source_results)
    source_result_dict[key] = (source, per_reliable, per_unbiased, url)
  return source_result_dict

# Main
if __name__ == "__main__":
  output = OrderedDict()
  json_filename = os.path.join("static", "output.json")

  if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
    with open(sys.argv[1], 'r') as f:
      urls = []
      for url in f.readlines():
        urls.append(url)

  output["urls"] = []

  for url in urls:
    try:
      parse_url(output, url)
    except Exception as e:
      print e

  with open(json_filename, 'w') as outfile:
    json.dump(output, outfile, indent=2)
