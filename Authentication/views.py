# authentication.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from rest_framework.views import APIView
from rest_framework import status
from .serializers import AvatarUploadSerializer
from django.conf import settings
from . import models

import logging

logger = logging.getLogger(__name__)



User = get_user_model()

class WechatAuthBackend(ModelBackend):
    def authenticate(self, request, openid=None, **kwargs):
        if openid:
            try:
                user = User.objects.get(openID=openid)
                return user
            except User.DoesNotExist:
                # User matching the openid was not found
                return None
        # For admin site authentication
        return super().authenticate(request, **kwargs)
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None




@api_view(['POST'])
def wechat_login(request):
    code = request.data.get('code')
    if not code:
        return Response({'error': 'Code is required'}, status=400)
    
    try:
        WxUser = get_WxUser_from_wechat(code)
        if not WxUser:
            return Response({'error': 'Invalid code'}, status=400)

        openID = WxUser.get('openid')
        session_key = WxUser.get('session_key')

        user, created = models.User.objects.get_or_create(
            openID=openID, 
            defaults={'session_key': session_key}
        )

        # 认证用户
        backend = WechatAuthBackend()
        user = backend.authenticate(request, openid=openID)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'created': not created
            }, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

    return Response({'error': 'Invalid code'}, status=400)

def get_WxUser_from_wechat(code):
    if settings.DEBUG:
        if code.startswith('test'):
        # 本地测试时，直接返回测试用的 openid
            return {'openid': code}
    code2Session= "https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code"
    response = requests.get(code2Session.format(settings.APPID, settings.APPSECRET, code))
    data = response.json()
    logger.debug("wx api: " + str(data))
    if data.get("openid"):
        return data
    else:
        return False




# views.py
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class UserInfoAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # 返回当前认证用户的实例
        return self.request.user



class AvatarUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = AvatarUploadSerializer(user, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# example how to utilize the auth decorator

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def test_view(request):
    return Response('OK')



