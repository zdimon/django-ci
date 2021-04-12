from django.urls import path
from .views import *
urlpatterns = [
    path('list', list),
    path('pre_remove/<int: id>', pre_remove),
]
