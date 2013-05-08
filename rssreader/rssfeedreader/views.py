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

    # This block handles adding, editing, and removal of feeds.
    if 'addFeed' in request.POST:
        userErrors.append(addFeed(request))
    elif 'editFeed' in request.POST:
        userErrors.append(editFeed(request))
    elif 'removeFeed' in request.POST:
        userErrors.append(removeFeed(request))

    #If user is already logged in, pass along user information to be displayed.
    if 'username' in request.session:
        if 'userid' in request.session:
            userFeeds = feeds.objects.filter(userid=request.session['userid'])
            
            for feedInfo in userFeeds:
                userRSSList.append([feedInfo.name, feedInfo.url, feedInfo.id, parseRSS(feedInfo.url)])

            context = RequestContext(request, {"userName":request.session['username'], \
                                               "userRSSList":userRSSList, \
                                               'userErrors':userErrors}) 
    else:
        context = RequestContext(request, {'userErrors':userErrors})   
 
    return HttpResponse(template.render(context))
