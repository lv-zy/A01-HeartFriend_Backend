from django.urls import path, re_path
from django.contrib import admin 
from . import views 


urlpatterns = [ 
    path('', views.DiaryList.as_view(), name="diary-list-user"), 
    re_path(r'^(?P<pk>[0-9]+)$', views.DiaryDetail.as_view(), name="diary-detail"),
    path('upload-image/', views.ImageUploadView.as_view(), name='upload-image'), 
]