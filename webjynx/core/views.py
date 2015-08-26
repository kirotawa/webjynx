#-*-  coding: utf-8 -*-

from django.shortcuts import render
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as sigin, logout as signoff
from core.utils import *
from core.models import *
from core.forms import *


def register(request):
    context = RequestContext(request)

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            messages.add_message(request, messages.SUCCESS, 'User registered')
            return redirect('/login/')

        else:
            print user_form.errors
    else:
        user_form = UserForm()

    return render_to_response('register.html', locals(),
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def logout(request):
    signoff(request)
    return redirect('/login/')


def login(request):
    logout(request)
    usermail = password = ''
    user = None

    if request.POST:
        usermail = request.POST['useremail']
        password = request.POST['password']

        usr = User.objects.get(email=usermail)
        if usr:
            user = authenticate(username=usr.username, password=password)

        if user is not None:
            if user.is_active:
                sigin(request, user)
                return redirect('main', user_id=usr.id)

        else:
            messages.add_message(request, messages.ERROR, 'Login failed.')
            return redirect('/login/')

    return render_to_response('login.html', locals(),
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def main(request, user_id):
    repositories = Repositories.objects.all()
    repo_pk = "Repositories"
    sha_list = ""
    user = User.objects.get(id=user_id)

    if not user:
        messages.add_message(request, messages.ERROR, 'Invalid user')
        return redirect('/login/')

    if request.method == "POST":
        if 'file' in request.POST.keys() and 'sha' not in request.POST.keys():
            file_ = request.POST['file']
            if 'repository' in request.POST.keys():
                repo_pk = request.POST['repository']
                repository = get_object_or_404(Repositories, pk=repo_pk)
                sha_list = get_commit_shas(file_, repository.path_name)
            else:
                sha_list = [""]

        elif 'sha' in request.POST.keys():
            shas = request.POST['shas'].split(' ')[1:]
            msgs = request.POST['msg'].split('^$')[1:]
            sha_list = []

            for i, sha in enumerate(shas):
                sha_list.append([sha, msgs[i]])

            file_ = request.POST['file']
            sha_clicked = request.POST['sha']
            repo_pk = request.POST['repository']
            repository = get_object_or_404(Repositories, pk=repo_pk)
            code_patch = get_patch(sha_clicked, repository.path_name)

            # TODO: find another way and delete this ugly workaround
            code_patch = code_patch.decode('iso-8859-1')

    return render_to_response('main.html', locals(),
                              context_instance=RequestContext(request))


def addrepo(request):
    repo_to_save = Repositories()
    if request.method == "POST":
        if 'reponame' in request.POST.keys():
            repo_to_save.name = request.POST['reponame']
            repo_to_save.path_name = request.POST['repopath']
            repo_to_save.user = User.objects.get(username=request.POST['user'])
            repo_to_save.save()

            repositories = Repositories.objects.all()

    return render_to_response('main.html', locals(),
                              context_instance=RequestContext(request))


#def index(request):
#    return HttpResponse("")
