# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from rssfeedreader.models import users, feeds

def index(request):
	userInfo = users.objects.filter(username='swillis16')

	if userInfo:
		rssList = feeds.objects.filter(userid=userInfo[0].id)

	context = Context({"userName":userInfo[0].username, "userRssList":rssList})

	template = loader.get_template('rssfeedreader/index.html')
	return HttpResponse(template.render(context))
