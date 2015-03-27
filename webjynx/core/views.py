from django.shortcuts import render
from django.contrib import messages, auth
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from core.utils import *
from core.models import *


def main(request):
    repositories = Repositories.objects.all()
    repo_pk = "Repositories"
    sha_list = ""

    if request.method == "POST":
        if 'file' in request.POST.keys() and 'sha' not in request.POST.keys():
            file_ = request.POST['file']
            repo_pk = request.POST['repository']
            repository = get_object_or_404(Repositories, pk=repo_pk)
            sha_list = get_commit_shas(file_, repository.path_name)

        elif 'sha' in request.POST.keys():
            sha_list = request.POST['shas'].split(' ')[1:]
            file_ = request.POST['file']
            sha = request.POST['sha']
            repo_pk = request.POST['repository']
            repository = get_object_or_404(Repositories, pk=repo_pk)
            code_patch = get_patch(sha, repository.path_name)

    return render_to_response('base.html', locals(),
                              context_instance=RequestContext(request))


def addrepo(request):
    repo_to_save = Repositories()

    if request.method == "POST":
        if 'reponame' in request.POST.keys():
            repo_to_save.name = request.POST['reponame']
            repo_to_save.path_name = request.POST['repopath']
            repo_to_save.save()
            repositories = Repositories.objects.all()

    return render_to_response('base.html', locals(),
                              context_instance=RequestContext(request))


def index(request):
    return HttpResponse("")
