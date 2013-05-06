# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from rssfeedreader.models import users, feeds
# Stores various functions needed for views.
from utils import *
import hashlib
from urlparse import urlparse

# View for index page.
def index(request):
    template = loader.get_template('rssfeedreader/index.html') 
    context = RequestContext(request, {})
    userErrors = []
    userRSSList = []

    if 'logout' in request.GET:
        return logout(request)
        
    #If user has submitted form, check login information or registration information.
    if ('username' in request.POST) and ('password' in request.POST):
            userNameInput = request.POST['username']
            passwordInput = hashlib.sha224(request.POST['password']).hexdigest()

            if request.POST['submit'] == 'Login':
                result = loginUser(userNameInput, passwordInput, request)
                if result:
                    userErrors.append(result)

            if request.POST['submit'] == 'Register':
                result = registerUser(userNameInput, passwordInput, request)
                if result:
                    userErrors.append(result)

    # This block handles adding of feeds.
    if 'submit' in request.POST and 'feedURL' in request.POST:
        if not urlparse(request.POST['feedURL']).hostname:
             userErrors.append('The url entered is invalid.')

        if not request.POST['siteName']:
            userErrors.append('No site name is given.')

        if urlparse(request.POST['feedURL']).hostname and request.POST['siteName']:
            feed = feeds(url=request.POST['feedURL'], name=request.POST['siteName'])
            feed.save()
            feed.userid.add(request.session['userid'])
            feed.save()

    #If user is already logged in, pass along user information to be displayed.
    if 'username' in request.session:
        if 'userid' in request.session:
            userFeeds = feeds.objects.filter(userid=request.session['userid'])
            
            for feedInfo in userFeeds:
                userRSSList.append(parseRSS(feedInfo.url))

            context = RequestContext(request, {"userName":request.session['username'], \
                                               "userRSSList":userRSSList, \
                                               'userErrors':userErrors}) 
    
    return HttpResponse(template.render(context))
