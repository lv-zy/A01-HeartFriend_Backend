from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
import uuid


class UserDetailTest(APITestCase):
    def mylogin(self, user):
        self.user_data = {'username': user.username, 'code': user.openID}
        response = self.client.post('/api/v1/user/login/', self.user_data, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

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
        self.mylogin(self.user)
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


from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient

User = get_user_model()

class UserFollowTests(APITestCase):
    def mylogin(self, user):
        self.user_data = {'username': user.username, 'code': user.openID}
        response = self.client.post('/api/v1/user/login/', self.user_data, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def follow(self, user1, user2):
        self.mylogin(user1)
        self.client.post(reverse('follow-unfollow', kwargs={'uuid': user2.uuid}))
        self.client.credentials(HTTP_AUTHORIZATION = '')

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser', openID = 'testopenid')
        self.user2 = User.objects.create_user(username='testuser2', openID = 'testopenid2')
        self.user3 = User.objects.create_user(username='testuser3', openID = 'testopenid3')
        self.user4 = User.objects.create_user(username='testuser4', openID = 'testopenid4')

        self.follow(self.user1, self.user2)
        self.follow(self.user1, self.user3)
        self.follow(self.user2, self.user1)
        self.follow(self.user2, self.user3)
        self.follow(self.user3, self.user4)
        



        self.client = APIClient()

    def test_follow_unfollow_user(self):
        # User1 follows User2
        self.mylogin(self.user1)
        self.assertTrue(self.user1.is_following(self.user2))

        # User1 unfollows User2
        response = self.client.post(reverse('follow-unfollow', kwargs={'uuid': self.user2.uuid}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user1.is_following(self.user2))

        
        invalid_uuid = '12345678-1234-1234-1234-1234567890ab'
        response = self.client.post(reverse('follow-unfollow', kwargs={'uuid': invalid_uuid}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_self_info(self):
        self.mylogin(self.user1)
        response = self.client.get(reverse('user-info'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['following_count'], 2)
        self.assertEqual(response.data['followers_count'], 1)

        self.mylogin(self.user3)
        response = self.client.get(reverse('user-info'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['following_count'], 1)
        self.assertEqual(response.data['followers_count'], 2)

    def test_followers_list(self):
        self.mylogin(self.user1)
        response = self.client.get(reverse('followers-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['followers']), 1)
        self.assertEqual(response.data['followers'][0]['username'], self.user2.username)


        self.mylogin(self.user3)
        response = self.client.get(reverse('followers-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['followers']), 2)
        self.assertEqual(response.data['followers'][0]['username'], self.user1.username)
        self.assertEqual(response.data['followers'][1]['username'], self.user2.username)
    
    def test_following_list(self):
        self.mylogin(self.user1)
        response = self.client.get(reverse('following-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['following']), 2)
        self.assertEqual(response.data['following'][0]['username'], self.user2.username)
        self.assertEqual(response.data['following'][1]['username'], self.user3.username)


        self.mylogin(self.user3)
        response = self.client.get(reverse('following-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['following']), 1)
        self.assertEqual(response.data['following'][0]['username'], self.user4.username)
