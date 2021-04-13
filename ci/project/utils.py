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
        prj_dir = os.path.join(settings.ORIGIN_DIR, project.name, project.venv_path)
    else:
        prj_dir = os.path.join(settings.ORIGIN_DIR, project.name)
    
    tpl = tpl.replace('%prj_dir%', prj_dir)
    tpl = tpl.replace('%ci_dir%', str(settings.BASE_DIR))
    tpl = tpl.replace('%user%', settings.USER)
    if project.venv_path:
        tpl = tpl.replace('%env_dir%', os.path.join(settings.ORIGIN_DIR, project.name, project.venv_path, 'venv'))
    else:
        tpl = tpl.replace('%env_dir%', os.path.join(settings.ORIGIN_DIR, project.name, 'venv'))        
    filename = 'release-%s-django.conf' % project.name
    conf_path = os.path.join(
        settings.BASE_DIR, 'env-conf', 'supervisor', filename)
    with open(conf_path, 'w+') as f:
        f.write(tpl)


def release_nginx_conf(project_id):
    from project.models import Project, ProjectProcess
    project = Project.objects.get(pk=project_id)
    path = os.path.join(settings.BASE_DIR, 'tpl', 'nginx_vhost.conf')
    with open(path, 'r') as f:
        tpl = f.read()

    tpl = tpl.replace('%media_path%', project.media_path)
    sname = 'release-%s.%s' % (project.name, settings.DOMAIN)
    tpl = tpl.replace('%server_name%', sname)
    dj = ProjectProcess.objects.get(project=project, name='django')
    tpl = tpl.replace('%port%', str(dj.port))
    conf_path = os.path.join(
        settings.BASE_DIR, 'env-conf','nginx', sname)
    with open(conf_path, 'w+') as f:
        f.write(tpl) 


def frontend_conf(project_id):
    from project.models import Project, ProjectProcess
    project = Project.objects.get(pk=project_id)
    try:
        for pp in ProjectProcess.objects.filter(project=project, name='frontend'):
            path = os.path.join(settings.BASE_DIR, 'tpl', 'frontend.conf')
            with open(path, 'r') as f:
                tpl = f.read()
            sname = 'release-%s.frontend.%s' % (project.name, settings.DOMAIN)
            tpl = tpl.replace('%name%', sname)
            tpl = tpl.replace('%user%', settings.USER)
            prj_dir = os.path.join(settings.WORK_DIR, project.name, pp.path)
            tpl = tpl.replace('%prj_dir%', prj_dir)
            tpl = tpl.replace('%ci_dir%', str(settings.BASE_DIR))
            tpl = tpl.replace('%command%', pp.command)
            filename = 'release-%s-frontend.conf' % project.name
            conf_path = os.path.join(
                settings.BASE_DIR, 'env-conf', 'supervisor', filename)
            with open(conf_path, 'w+') as f:
                f.write(tpl)
    except Exception as e:
        print('Error in creating frontend supervisor conf!!!!! %s - %s' % (pp.path, pp.id))
        print(e)
