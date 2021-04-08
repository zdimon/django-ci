from django.urls import path
from .views import *
urlpatterns = [
    path('create', create),
    path('list', list),
    path('pre_create/<int:id>', pre_create),
    path('detail/<int:id>', detail),
    path('create/<int:id>', create),
]
