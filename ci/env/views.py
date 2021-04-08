from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project.models import Project, ProjectProcess
from .models import Environ, EnvironProcess
from django.shortcuts import redirect
from django.contrib import messages
from .tasks import generate_env, create_env


@login_required
def pre_create(request,id):
    project = Project.objects.get(pk=id)
    return render(request, 'env/pre_create.html', {'project':project})


@login_required
def create(request,id):
    if not create_env(id,request.user.id):
        messages.success(
            request, 'Ошибка. Эта область уже создана!')
    else:
        messages.success(
            request, 'Рабочая область создается. Это может занять 10-20 сек!')
    return redirect('/project/list')