from django.urls import path
from .views import *
urlpatterns = [
    path('create', create),
    path('task/create/<int:id>', task_create),
    path('task/detail/<int:id>', task_detail),
    path('list', list),
    path('pre_create/<int:id>', pre_create),
    path('pre_remove/<int:id>', pre_remove),
    path('remove/<int:id>', remove),
    path('detail/<int:id>', detail),
    path('create/<int:id>', create),
    path('merge/<int:id>', do_merge),
    path('build_front/<int:id>', do_build_front),
]
