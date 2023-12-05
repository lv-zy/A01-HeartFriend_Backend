from django.urls import path
from .views import wechat_login, UserInfoAPIView, AvatarUploadView, UserDetailView, FollowUnfollowView, FollowersListView, FollowingListView

urlpatterns = [
    path('login/', wechat_login, name='wechat_login'),
    path('info/', UserInfoAPIView.as_view(), name='user-info'),
    path('upload-avatar/', AvatarUploadView.as_view(), name='upload-avatar'),
    path('query-info/', UserDetailView.as_view(), name='user-detail'),
    path('follow-unfollow/', FollowUnfollowView.as_view(), name='follow-unfollow'),
    path('followers/', FollowersListView.as_view(), name='followers-list'),
    path('following/', FollowingListView.as_view(), name='following-list'),
]





