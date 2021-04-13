from django.conf import settings


def release_django_conf(project_id):
    from .models import Environ, EnvironProcess
    env = Environ.objects.get(pk=env_id)
    envp = EnvironProcess.objects.get(env=env, name='django')
    path = os.path.join(settings.BASE_DIR, 'tpl', 'django.conf')
    with open(path, 'r') as f:
        tpl = f.read()
    sname = '%s.django.%s' % (env.name, settings.DOMAIN)
    tpl = tpl.replace('%name%', sname)
    tpl = tpl.replace('%port%', str(envp.port))
    if env.project.venv_path:
        prj_dir = os.path.join(settings.WORK_DIR, env.name, env.project.venv_path)
    else:
        prj_dir = os.path.join(settings.WORK_DIR, env.name)
    
    tpl = tpl.replace('%prj_dir%', prj_dir)
    tpl = tpl.replace('%ci_dir%', str(settings.BASE_DIR))
    tpl = tpl.replace('%user%', settings.USER)
    if env.project.venv_path:
        tpl = tpl.replace('%env_dir%', os.path.join(settings.WORK_DIR, env.name, env.project.venv_path, 'venv'))
    else:
        tpl = tpl.replace('%env_dir%', os.path.join(settings.WORK_DIR, env.name, 'venv'))        
    filename = '%s-django.conf' % env.name
    conf_path = os.path.join(
        settings.BASE_DIR, 'env-conf', 'supervisor', filename)
    with open(conf_path, 'w+') as f:
        f.write(tpl)
