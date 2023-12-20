from django.contrib import admin
from django.urls import path, include
from .views import countm1, countm2

urlpatterns = [
    path('count/m1', countm1, name='count-m1'), 
    path('count/m2', countm2, name='count-m2'),
]
