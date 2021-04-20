"""ci URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from main.views import index, done, logout_view, env, tasks, take_task, del_task, done_task, end_task, instr, hook, merge_master, maket, set_language
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('done/<int:id>', done),
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('logout', logout_view),
    path('env', env),
    path('tasks', tasks),
    path('instr', instr),
    path('hook', hook),
    path('maket/<int:id>', maket),
    path('task/take/<int:id>', take_task),
    path('task/del/<int:id>', del_task),
    path('task/done/<int:id>', done_task),
    path('task/end/<int:id>', end_task),
    path('set/language', set_language),
    #path('env/merge/<int:id>', merge_master),
    path('tinymce/', include('tinymce.urls')),
    path('rosetta/', include('rosetta.urls')),
]

urlpatterns += i18n_patterns(
    path('', index),
    path('', include('account.urls')),
    path('', include('control.urls')),
    path('project/', include('project.urls')),
    path('env/', include('env.urls')),
)



urlpatterns = urlpatterns + static(settings.MEDIA_URL,
                                   document_root=settings.MEDIA_ROOT)

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)