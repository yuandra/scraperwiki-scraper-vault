###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2


QUERY = '#ReplacetaglinewithJokowi'
GEOINFO = '53.26521293124656,-9.063720703125,257km'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 15 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
% (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data['from_user_id_str'] = result['from_user_id_str']
            data['created_at'] = result['created_at']
            data['from_user'] = result['from_user']
            data['id_str'] = result['id_str']
            data['metadata'] = result['metadata']
            data['to_user_id'] = result['to_user_id']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data)

    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    ###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2


QUERY = '#ReplacetaglinewithJokowi'
GEOINFO = '53.26521293124656,-9.063720703125,257km'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 15 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
% (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data['from_user_id_str'] = result['from_user_id_str']
            data['created_at'] = result['created_at']
            data['from_user'] = result['from_user']
            data['id_str'] = result['id_str']
            data['metadata'] = result['metadata']
            data['to_user_id'] = result['to_user_id']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data)

    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    