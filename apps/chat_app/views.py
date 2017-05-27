from django.shortcuts import render, redirect, HttpResponse
from .models import User, Secret
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def index(request):
    return render(request, 'chat_app/index.html')

def register(request):
    if request.method == "GET":
        return redirect("/")
    newuser = User.objects.validate(request.POST)
    print newuser
    if newuser[0] == False:
        for each in newuser[1]:
            messages.error(request, each)#for each error in the array, make a message for each one
        return redirect("/")
    if newuser[0] == True:
        messages.success(request, 'Successfully registred, you may log in')
        request.session['userid'] = newuser[1].id
        return redirect ('/secrets')

def login(request):
    if request.method=="GET":
        return redirect('/')
    login = User.objects.login(request.POST['username'])
    if login[0]:
        request.session['id'] = login[1].id
        return redirect('/secrets')
    messages.error(request, login[1], extra_tags = "login")
    return redirect('/')

def process(request):
    if request.method=="GET":
        return redirect('/')
    print "In the process, going to make a secret", request.POST
    result = Secret.objects.validate(request.POST['secret'], request.session['id'])
    if result[0]:
        messages.info(request, result[1])
        return redirect('/secrets')
    messages.error(request, result[1])
    return redirect('/secrets')


def secrets(request):
    if checkForLogin(request):
        # collect all secrets and send to the template
        allsecrets = Secret.objects.all().order_by('-id')[:5]
        context = {
            "secrets" : allsecrets,
            "currentuser" : User.objects.get(id=request.session['id'])
        }

        return render(request, 'chat_app/secrets.html', context)
    else:
        return redirect('/')

def newlike(request, id, sentby):
    # we are receiving the id of the secret
    print "we are in the new like", id
    result = Secret.objects.newlike(id, request.session['id'])
    if result[0] == False:
        messages.error(request, result[1])
    if sentby == "sec":
        return redirect('/secrets')
    else:
        return redirect('/popular')

def delete(request, id, sentby):
    print "we are in the delete", id
    result = Secret.objects.deleteLike(id, request.session['id'])
    if result[0] == False:
        messages.error(request, result[1])
    if sentby == "sec":
        return redirect('/secrets')
    else:
        return redirect('/popular')

def popular(request):
    if checkForLogin(request):
        allsecrets = Secret.objects.annotate(num_likes=Count('likers')).order_by('-num_likes')
        context = {
            "secrets" : allsecrets,
            "currentuser" : User.objects.get(id=request.session['id'])
        }
        return render(request, 'chat_app/popular.html', context)
    else:
        return redirect('/')


def logout(request):
    request.session.pop('id')
    return redirect('/')


def checkForLogin(request):
    if 'id' not in request.session:
        messages.error(request, "You must login to view the requested page", extra_tags="register")
        return False
    return True
