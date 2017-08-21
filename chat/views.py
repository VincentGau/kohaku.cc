from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'haku_chat/home.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['userid']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/chat/chat_room')
        else:
            return HttpResponseRedirect('/chat')

    return HttpResponseRedirect('/chat')


@login_required(login_url="/chat/login/")
def chat_room(request):
    user = request.user
    if not user:
        return HttpResponseRedirect('/chat')
    return render(request, 'haku_chat/chat_room.html', {'username': user.username})
