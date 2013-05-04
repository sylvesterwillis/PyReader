# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from rssfeedreader.models import users, feeds
import hashlib

def index(request):
    template = loader.get_template('rssfeedreader/index.html') 
    context = RequestContext(request, {})
    userErrors = []

    if 'logout' in request.GET:
        try:
            del request.session['username']
            del request.session['userid']
            userErrors.append('You have logged out.')
        except KeyError:
            userErrors.append('You have already logged out.')

        context = RequestContext(request, {'userErrors':userErrors, 'loggedout':True})
        return HttpResponseRedirect('/rssfeedreader/')    
        
    #If user has submitted form, check login information or registration information.
    if ('username' in request.POST) and ('password' in request.POST):
            userNameInput = request.POST['username']
            passwordInput = hashlib.sha224(request.POST['password']).hexdigest()

            if request.POST['submit'] == 'Login':
                userInfo = users.objects.filter(username=userNameInput, password=passwordInput)
                # Store information in session to make processing easier when the user has logged in, registered, 
                # or accessed the page with the information within session.
                if userInfo.count() > 0:
                    request.session['username'] = userInfo[0].username
                    request.session['userid'] = userInfo[0].id
                else:
                    userErrors.append('Username or password is incorrect.')

            if request.POST['submit'] == 'Register':
                userInfo = users.objects.filter(username=userNameInput)
                
                if userInfo.count() > 0:
                    userErrors.append('Username already exists.')
                else:
                    user = users(username=userNameInput, password=passwordInput)
                    user.save()
                    request.session['username'] = user.username
                    request.session['userid'] = user.id


    #If user is already logged in, pass along useddr information to be displayed.
    if 'username' in request.session:
        if 'userid' in request.session:
            rssList = feeds.objects.filter(userid=request.session['userid'])
            context = RequestContext(request, {"userName":request.session['username'], "userRssList":rssList})
    else:
            context = RequestContext(request, {'userErrors':userErrors})
        
    
    return HttpResponse(template.render(context))
