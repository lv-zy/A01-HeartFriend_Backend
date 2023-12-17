from django.urls import path, re_path
from django.contrib import admin 
from . import views 


urlpatterns = [ 
    path('', views.ChatView.as_view(), name="invoke-ai-chat"),
]