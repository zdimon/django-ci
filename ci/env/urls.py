from django.urls import path
from .views import *
urlpatterns = [
    path('create', create),
    path('list', list),
    path('pre_create/<int:id>', pre_create),
    path('pre_remove/<int:id>', pre_remove),
    path('remove/<int:id>', remove),
    path('detail/<int:id>', detail),
    path('create/<int:id>', create),
]
