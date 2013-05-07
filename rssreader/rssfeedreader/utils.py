# This file hosts helper functions for the views.
import requests
from bs4 import BeautifulSoup
import HTMLParser
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from rssfeedreader.models import users, feeds
from urlparse import urlparse

class RSSItem:
    title = ''
    link = ''
    comments = ''
    pubDate = ''

# This function takes a url to an RSS feed, parse said feed and returns 
# a list of content for the feed. Also, it is reccommended that lxml is 
# installed.
def parseRSS(url):
    # OutputItems contaions a site title and its corresponding RSS info.
    outputItems = {}

    #Opening XML from url.
    try:
        xml = requests.get(url).text
    except requests.HTTPError, e:
        outputItems['requestError'] = "There was an HTTP error: " + e.code
        return outputItems
    except requests.ConnectionError, e:
        outputItems['requestError'] = "A connection error occurred."
        return outputItems

    #Storing XML in BeautifulSoup object.
    soup = BeautifulSoup(xml, "xml")

    # Check if document is an rss document.
    if soup.find("rss") == 'None':
        return 'This RSS page is not available.'

    # Using RSS standard to find all items and site title.
    itemList = soup.find_all('item')
    siteTitle = soup.title.contents[0].encode('utf-8')
    
    # Creating array for site RSS info.
    outputItems[siteTitle] = []
    
    numberOfItemsDisplayed = 10

    i = 0
    htmlParse = HTMLParser.HTMLParser()
    while i < numberOfItemsDisplayed and i < len(itemList):
        item = RSSItem()

        #Encoding needed for output strings.
        item.title = htmlParse.unescape(itemList[i].title.contents[0].encode('utf-8'))
        item.link = itemList[i].link.contents[0].encode('utf-8')

        # Show link to comments if exist.
        if itemList[i].comments:
            item.comments = itemList[i].comments.contents[0].encode('utf-8')
        
        if itemList[i].pubDate:
            item.pubDate = itemList[i].pubDate.contents[0].encode('utf-8')

        outputItems[siteTitle].append(item)
        i += 1

    return outputItems

def logout(request):
    template = loader.get_template('rssfeedreader/index.html')
    context = RequestContext(request, {})
    userErrors = []
    userRSSList = []

    try:
        del request.session['username']
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect('/rssfeedreader/')

def loginUser(userNameInput, passwordInput, request):
    userInfo = users.objects.filter(username=userNameInput, password=passwordInput)
    # Store information in session to make processing easier when the user has logged in, registered, 
    # or accessed the page with the information within session.
    if userInfo.count() > 0:
        request.session['username'] = userInfo[0].username
        request.session['userid'] = userInfo[0].id
        return ''
    else:
        return 'Username or password is incorrect.'

def registerUser(userNameInput, passwordInput, request):
    userInfo = users.objects.filter(username=userNameInput)

    if userInfo.count() > 0:
        return 'Username already exists.'
    else:
        user = users(username=userNameInput, password=passwordInput)
        user.save()
        request.session['username'] = user.username
        request.session['userid'] = user.id
        return ''
