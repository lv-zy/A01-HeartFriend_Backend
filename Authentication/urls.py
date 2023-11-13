from django.urls import path
from .views import test_view, wechat_login

urlpatterns = [
    path('login/', wechat_login, name='wechat_login'),
    path('test/', test_view, name='test')
]
