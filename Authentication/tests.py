from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
import uuid


class UserDetailTest(APITestCase):
    def setUp(self):
        # 创建一个新用户
        self.user = User.objects.create_user(
            openID='12345', 
            username='testuser', 
            gender='male', 
            self_intro='Hello world!', 
            age=25
        )
        # ... 初始化其他字段 ...

    def test_get_user_by_uuid(self):
        # 获取用户详情的 URL
        url = reverse('user-detail', kwargs={'uuid': self.user.uuid})
        
        # 发送 GET 请求
        response = self.client.get(url)

        # 校验响应状态码
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 校验返回的数据
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['gender'], self.user.gender)
        self.assertEqual(response.data['self_intro'], self.user.self_intro)
        self.assertEqual(response.data['age'], self.user.age)
