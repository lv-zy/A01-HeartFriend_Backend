from django.urls import path
from .views import test_view, wechat_login, UserInfoAPIView, AvatarUploadView

urlpatterns = [
    path('login/', wechat_login, name='wechat_login'),
    path('info/', UserInfoAPIView.as_view(), name='user-info'),
    path('test/', test_view, name='test'),
    path('upload-avatar/', AvatarUploadView.as_view(), name='upload-avatar'),
]





