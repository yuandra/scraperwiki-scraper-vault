                         
import scraperwiki

# Blank Python

# typical URL is http://www.london-gazette.co.uk/id/issues/60112/notices/1568529
# list of URLs collected by scraper at https://scraperwiki.com/scrapers/bankruptcies/
# Downloaded as CSV and codes extracted in Google Docs by using =RIGHT(A2, 7)
# Cycle through a list of those codes, created by using the =JOIN formula in Google Docs

#If you want to understand this scraper - start at the bottom where it says 'base_url'

import scraperwiki
#import urlparse
import lxml.html
from lxml import etree

#TM - set debug on or off
debug = False

# search for a span property by XPath
def search_by_span_attribute(root, attribute, value):
    foundVal = root.xpath("//span[@" + attribute + "='" + value + "']")
    if foundVal:
        if debug:
            print attribute + " " + value + " found with text: " + foundVal[0].text
        return foundVal[0].text
    else:
        if debug:
            print attribute + " not found."
        return ""

# custom search
def search_xpath(root, xpath):
    foundVal = root.xpath(xpath)
    if foundVal:
        if debug:
            print xpath + " returned text: " + foundVal[0].text
        return foundVal[0].text
    else:
        if debug:
            print xpath + " returned no results found."
        return ""

#Create a function called 'scrape_table' which is called in the function 'scrape_page' below
#The 'scrape_page' function also passed the contents of the page to this function as 'root'
def scrape_table(root):
    #Create a new empty record
    record = {}

    record['pubdate'] = search_by_span_attribute(root, "property", "g:hasPublicationDate")
    record['noticecode'] = search_by_span_attribute(root, "property", "g:hasNoticeCode")
    #TM - you'll need to look for an example of this from page source when you come across one that should have it... unless it is the same as court:courtName below?
    #record['registry'] = search_by_span_attribute(root, "property",
    record['company number'] = search_by_span_attribute(root, "property", "organisation:companyNumber")
    record['company name'] = search_by_span_attribute(root, "property", "organisation:name")
    record['nature of business'] = search_by_span_attribute(root, "property", "organisation:natureOfBusiness")
    #record['trade classification'] = search_by_span_attribute(root, "property",
    record['date of appointment'] = search_by_span_attribute(root, "property", "corp-insolvency:dateOfAppointment")
    #TM - this one is a bit special as there are two that match it if you search for just the "vCard:label" property. To guarantee the right one, we have to customize the XPath a bit...
    record['registered office of company'] = search_xpath(root, "//span[@rel='organisation:hasRegisteredOffice']//span[@property='vCard:label']")
    record['principle trading adddress'] = search_xpath(root, "//span[@rel='organisation:hasPrincipalTradingAddress']//span[@property='vCard:label']")
    #record['sector'] = search_by_span_attribute(root, "property",
    record['date of appointment'] = search_by_span_attribute(root, "property", "corp-insolvency:dateOfAppointment")
    record['court'] = search_by_span_attribute(root, "property", "court:courtName")
    #record['date'] = search_by_span_attribute(root, "property", #same as date?
    #record['urlcode'] = search_by_span_attribute(root, "property",
    record['ID'] = item

    scraperwiki.sqlite.save(["ID"], record)
       

#this creates a new function and (re)names whatever parameter is passed to it - i.e. 'next_link' below - as 'url'
def scrape_page(url):
    #now 'url' is scraped with the scraperwiki library imported above, and the contents put into a new object, 'html'
    html = scraperwiki.scrape(url)
    #TM - commented out the below print
    #print html
    #now we use the lxml.html function imported above to convert 'html' into a new object, 'root'
    #TM - except we are now using etree!
    #root = lxml.html.fromstring(html)
    root = etree.HTML(html)
    #now we call another function on root, which we write - above
    scrape_table(root)

#START HERE: This is the part of the URL which all our pages share
base_url = 'http://www.london-gazette.co.uk/id/issues/'

#And these are the numbers which we need to complete that URL to make each individual URL
#This array has been compiled using the =JOIN formula in Google Docs on a column of URL codes
codes =['60189/notices/1615529', '60193/notices/1618256', '60162/notices/1601716', '60164/notices/1602609', '60164/notices/1602655', '60164/notices/1603840', '60164/notices/1602667', '60165/notices/1603559', '60165/notices/1603056', '60165/notices/1603670', '60166/notices/1606805', '60166/notices/1605343', '60166/notices/1605315', '60166/notices/1606798', '60166/notices/1605328', '60166/notices/1605348', '60166/notices/1605268', '60170/notices/1607033', '60170/notices/1606471', '60171/notices/1609672', '60171/notices/1609673', '60171/notices/1609799', '60171/notices/1609800', '60171/notices/1609805', '60171/notices/1609806', '60171/notices/1609807', '60171/notices/1609808', '60171/notices/1609809', '60172/notices/1609299', '60172/notices/1608152', '60172/notices/1609137', '60172/notices/1610493', '60172/notices/1608121', '60172/notices/1608624', '60181/notices/1611197', '60181/notices/1611003', '60186/notices/1612059', '60186/notices/1612631', '60186/notices/1614556', '60187/notices/1613945', '60187/notices/1613986', '60187/notices/1613057', '60188/notices/1614304', '60188/notices/1616272', '60188/notices/1615041', '60188/notices/1614994', '60189/notices/1617042', '60193/notices/1618246', '60193/notices/1620073', '60193/notices/1620074', '60195/notices/1619339', '60195/notices/1619818', '60195/notices/1619798', '60164/notices/1603349', '60165/notices/1605745', '60166/notices/1606424', '60166/notices/1605306', '60166/notices/1605588', '60170/notices/1608367', '60170/notices/1607517', '60171/notices/1609530', '60181/notices/1611002', '60181/notices/1611058', '60186/notices/1614326', '60187/notices/1615369', '60187/notices/1613921', '60189/notices/1616741', '60193/notices/1619980']

#go through the schoolIDs array above, and for each ID...
for item in codes:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)


                         
import scraperwiki

# Blank Python

# typical URL is http://www.london-gazette.co.uk/id/issues/60112/notices/1568529
# list of URLs collected by scraper at https://scraperwiki.com/scrapers/bankruptcies/
# Downloaded as CSV and codes extracted in Google Docs by using =RIGHT(A2, 7)
# Cycle through a list of those codes, created by using the =JOIN formula in Google Docs

#If you want to understand this scraper - start at the bottom where it says 'base_url'

import scraperwiki
#import urlparse
import lxml.html
from lxml import etree

#TM - set debug on or off
debug = False

# search for a span property by XPath
def search_by_span_attribute(root, attribute, value):
    foundVal = root.xpath("//span[@" + attribute + "='" + value + "']")
    if foundVal:
        if debug:
            print attribute + " " + value + " found with text: " + foundVal[0].text
        return foundVal[0].text
    else:
        if debug:
            print attribute + " not found."
        return ""

# custom search
def search_xpath(root, xpath):
    foundVal = root.xpath(xpath)
    if foundVal:
        if debug:
            print xpath + " returned text: " + foundVal[0].text
        return foundVal[0].text
    else:
        if debug:
            print xpath + " returned no results found."
        return ""

#Create a function called 'scrape_table' which is called in the function 'scrape_page' below
#The 'scrape_page' function also passed the contents of the page to this function as 'root'
def scrape_table(root):
    #Create a new empty record
    record = {}

    record['pubdate'] = search_by_span_attribute(root, "property", "g:hasPublicationDate")
    record['noticecode'] = search_by_span_attribute(root, "property", "g:hasNoticeCode")
    #TM - you'll need to look for an example of this from page source when you come across one that should have it... unless it is the same as court:courtName below?
    #record['registry'] = search_by_span_attribute(root, "property",
    record['company number'] = search_by_span_attribute(root, "property", "organisation:companyNumber")
    record['company name'] = search_by_span_attribute(root, "property", "organisation:name")
    record['nature of business'] = search_by_span_attribute(root, "property", "organisation:natureOfBusiness")
    #record['trade classification'] = search_by_span_attribute(root, "property",
    record['date of appointment'] = search_by_span_attribute(root, "property", "corp-insolvency:dateOfAppointment")
    #TM - this one is a bit special as there are two that match it if you search for just the "vCard:label" property. To guarantee the right one, we have to customize the XPath a bit...
    record['registered office of company'] = search_xpath(root, "//span[@rel='organisation:hasRegisteredOffice']//span[@property='vCard:label']")
    record['principle trading adddress'] = search_xpath(root, "//span[@rel='organisation:hasPrincipalTradingAddress']//span[@property='vCard:label']")
    #record['sector'] = search_by_span_attribute(root, "property",
    record['date of appointment'] = search_by_span_attribute(root, "property", "corp-insolvency:dateOfAppointment")
    record['court'] = search_by_span_attribute(root, "property", "court:courtName")
    #record['date'] = search_by_span_attribute(root, "property", #same as date?
    #record['urlcode'] = search_by_span_attribute(root, "property",
    record['ID'] = item

    scraperwiki.sqlite.save(["ID"], record)
       

#this creates a new function and (re)names whatever parameter is passed to it - i.e. 'next_link' below - as 'url'
def scrape_page(url):
    #now 'url' is scraped with the scraperwiki library imported above, and the contents put into a new object, 'html'
    html = scraperwiki.scrape(url)
    #TM - commented out the below print
    #print html
    #now we use the lxml.html function imported above to convert 'html' into a new object, 'root'
    #TM - except we are now using etree!
    #root = lxml.html.fromstring(html)
    root = etree.HTML(html)
    #now we call another function on root, which we write - above
    scrape_table(root)

#START HERE: This is the part of the URL which all our pages share
base_url = 'http://www.london-gazette.co.uk/id/issues/'

#And these are the numbers which we need to complete that URL to make each individual URL
#This array has been compiled using the =JOIN formula in Google Docs on a column of URL codes
codes =['60189/notices/1615529', '60193/notices/1618256', '60162/notices/1601716', '60164/notices/1602609', '60164/notices/1602655', '60164/notices/1603840', '60164/notices/1602667', '60165/notices/1603559', '60165/notices/1603056', '60165/notices/1603670', '60166/notices/1606805', '60166/notices/1605343', '60166/notices/1605315', '60166/notices/1606798', '60166/notices/1605328', '60166/notices/1605348', '60166/notices/1605268', '60170/notices/1607033', '60170/notices/1606471', '60171/notices/1609672', '60171/notices/1609673', '60171/notices/1609799', '60171/notices/1609800', '60171/notices/1609805', '60171/notices/1609806', '60171/notices/1609807', '60171/notices/1609808', '60171/notices/1609809', '60172/notices/1609299', '60172/notices/1608152', '60172/notices/1609137', '60172/notices/1610493', '60172/notices/1608121', '60172/notices/1608624', '60181/notices/1611197', '60181/notices/1611003', '60186/notices/1612059', '60186/notices/1612631', '60186/notices/1614556', '60187/notices/1613945', '60187/notices/1613986', '60187/notices/1613057', '60188/notices/1614304', '60188/notices/1616272', '60188/notices/1615041', '60188/notices/1614994', '60189/notices/1617042', '60193/notices/1618246', '60193/notices/1620073', '60193/notices/1620074', '60195/notices/1619339', '60195/notices/1619818', '60195/notices/1619798', '60164/notices/1603349', '60165/notices/1605745', '60166/notices/1606424', '60166/notices/1605306', '60166/notices/1605588', '60170/notices/1608367', '60170/notices/1607517', '60171/notices/1609530', '60181/notices/1611002', '60181/notices/1611058', '60186/notices/1614326', '60187/notices/1615369', '60187/notices/1613921', '60189/notices/1616741', '60193/notices/1619980']

#go through the schoolIDs array above, and for each ID...
for item in codes:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)


