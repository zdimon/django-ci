from django.urls import path
from .views import *
urlpatterns = [
    path('create', create),
    path('pre_create/<int:id>', pre_create),
    path('create/<int:id>', create),
]
