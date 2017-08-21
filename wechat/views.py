from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import hashlib

def index(request):
    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echostr = request.GET.get('echostr', None)

    token = 'wechatToken'

    hashlist = [token, timestamp, nonce]
    hashlist.sort()

    hashstr = ''.join([s for s in hashlist])

    hashstr = hashlib.sha1(hashstr).hexdigest()

    if hashstr == signature:
        return HttpResponse(echostr)

        # return HttpResponse("<a href='/hpc'>wechat<a>")
        # return HttpResponseRedirect('vote_TJ')
        # return render(request, 'hpc/index.html')
