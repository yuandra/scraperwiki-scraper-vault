#######################################################################################################################
# Twitter API scraper - Scrapping twitter for dataset to be used for sentiment analysis and data visualization         
#######################################################################################################################

import scraperwiki
import simplejson
import urllib2
import time


QUERY = 'ipl OR srh OR csk or rr OR dd OR rcb OR kkr OR mi OR kxip'
GEOINFO = '91.26521293124656,-91.063720703125,257km'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 15

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        #print err