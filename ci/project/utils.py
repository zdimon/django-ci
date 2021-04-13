from django.conf import settings
import os


def release_django_conf(project_id):
    from project.models import Project, ProjectProcess
    project = Project.objects.get(pk=project_id)
    pp = ProjectProcess.objects.get(project=project, name='django')
    path = os.path.join(settings.BASE_DIR, 'tpl', 'django.conf')
    with open(path, 'r') as f:
        tpl = f.read()
    sname = 'release-%s.django.%s' % (project.name, settings.DOMAIN)
    tpl = tpl.replace('%name%', sname)
    tpl = tpl.replace('%port%', str(pp.port))
    if project.venv_path:
        prj_dir = os.path.join(settings.WORK_DIR, project.name, project.venv_path)
    else:
        prj_dir = os.path.join(settings.WORK_DIR, project.name)
    
    tpl = tpl.replace('%prj_dir%', prj_dir)
    tpl = tpl.replace('%ci_dir%', str(settings.BASE_DIR))
    tpl = tpl.replace('%user%', settings.USER)
    if project.venv_path:
        tpl = tpl.replace('%env_dir%', os.path.join(settings.WORK_DIR, project.name, project.venv_path, 'venv'))
    else:
        tpl = tpl.replace('%env_dir%', os.path.join(settings.WORK_DIR, project.name, 'venv'))        
    filename = 'release-%s-django.conf' % project.name
    conf_path = os.path.join(
        settings.BASE_DIR, 'env-conf', 'supervisor', filename)
    with open(conf_path, 'w+') as f:
        f.write(tpl)
