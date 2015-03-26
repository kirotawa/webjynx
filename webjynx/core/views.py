from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.shortcuts import render
from django.contrib import messages, auth
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from core.utils import *
from core.models import *


@csrf_exempt
def main(request):
    repositories = Repositories.objects.all()
    repo_pk = "Repositories"
    sha_list = ""

    if request.method == "POST":
        if request.POST.has_key('file') and not request.POST.has_key('sha'):
            file_ = request.POST['file']
            repo_pk = request.POST['repository']
            repository = get_object_or_404(Repositories, pk=repo_pk)
            sha_list = get_commit_shas(file_, repository.path_name)

        elif request.POST.has_key('sha'):
            sha_list = request.POST['shas'].split(' ')[1:]
            file_ = request.POST['file']
            sha = request.POST['sha']
            repo_pk = request.POST['repository']
            repository = get_object_or_404(Repositories, pk=repo_pk)
            code_patch = get_patch(sha, repository.path_name)

    return render_to_response('base.html', locals(),
                              context_instance=RequestContext(request))


def index(request):
    return HttpResponse("")
