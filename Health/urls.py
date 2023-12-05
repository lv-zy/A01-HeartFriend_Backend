from django.urls import path, re_path
from django.contrib import admin 
from . import views 


urlpatterns = [ 
    path('', views.MedicineList.as_view(), name="medicine-list-user"), 
    re_path(r'^(?P<pk>[0-9]+)$', views.MedicineDetail.as_view(), name="medicine-detail"), 
]