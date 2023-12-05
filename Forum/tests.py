from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import Post, Comment


class PostAPITests(APITestCase):
    def mylogin(self, user):

        self.user_data = {'username': user.username, 'code': user.openID}
        response = self.client.post('/api/v1/user/login/', self.user_data, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def getDetailPostUrl(self, pk):
        return reverse('post-detail', kwargs={'pk': pk})

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', openID = 'testopenid')
        self.user2 = User.objects.create_user(username='testuser2', openID = 'testopenid2')
        self.user3 = User.objects.create_user(username='testuser3', openID = 'testopenid3')
        self.user4 = User.objects.create_user(username='testuser4', openID = 'testopenid4')

        # 创建帖子
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.post2 = Post.objects.create(title='Test Post2', content='Test Content2', author=self.user2)
        self.post3 = Post.objects.create(title='Test Post3', content='Test Content3', author=self.user3)
        self.pos4 = Post.objects.create(title='Test Post4', content='Test Content4', author=self.user4)

        # 设置 URL
        self.create_url = reverse('post-list')
        self.detail_url = reverse('post-detail', kwargs={'pk': self.post.pk})

        

    def test_create_post(self):
        self.mylogin(self.user)
        data = {'title': 'New Post', 'content': 'Content of the new post'}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(Post.objects.get(id=5).title, 'New Post')
        self.assertEqual(Post.objects.get(id=5).author.username, self.user.username)

    # 测试获取帖子列表
    def test_get_posts(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        
        # 验证返回的数据
        post_response = response.data[1]
        self.assertEqual(post_response['title'], self.post2.title)
        self.assertEqual(post_response['content'], self.post2.content)
        self.assertEqual(post_response['author'], self.post2.author.username)


    # 测试删除帖子（仅自己的帖子）
    def test_delete_own_post(self):
        self.mylogin(self.user)
        response = self.client.delete(self.getDetailPostUrl(self.post.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 3)




    # 测试阻止删除他人的帖子
    def test_prevent_deleting_others_post(self):
        self.mylogin(self.user2)
        response = self.client.delete(self.getDetailPostUrl(self.post.pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)





class CommentAPITests(APITestCase):
    def mylogin(self, user):

        self.user_data = {'username': user.username, 'code': user.openID}
        response = self.client.post('/api/v1/user/login/', self.user_data, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def getDetailPostUrl(self, pk):
        return reverse('post-detail', kwargs={'pk': pk})

    def setUp(self):
        # 创建用户
        self.user = User.objects.create_user(username='testuser', openID = 'testopenid')
        self.user2 = User.objects.create_user(username='testuser2', openID = 'testopenid2')
        self.user3 = User.objects.create_user(username='testuser3', openID = 'testopenid3')
        self.user4 = User.objects.create_user(username='testuser4', openID = 'testopenid4')

        # 创建帖子
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.post2 = Post.objects.create(title='Test Post2', content='Test Content2', author=self.user2)
        self.post3 = Post.objects.create(title='Test Post3', content='Test Content3', author=self.user3)
        self.pos4 = Post.objects.create(title='Test Post4', content='Test Content4', author=self.user4)

        # 创建评论
        self.comment = Comment.objects.create(post=self.post, content='Test Comment, after post1', author=self.user)
        self.comment2 = Comment.objects.create(post=self.post2, content='Test Comment, after post2', author=self.user2)
        self.comment2_1 = Comment.objects.create(post=self.post2, content='Test Comment2, after post2', author=self.user2)
        self.comment3 = Comment.objects.create(post=self.post3, content='Test Comment, after post3', author=self.user3)

        # 设置 URL
        self.create_url = reverse('post-list')
        self.detail_url = reverse('post-detail', kwargs={'pk': self.post.pk})

        self.comment_create_url = reverse('comment-list')
        print("Created comments count:", Comment.objects.count())
        print("Comment IDs:", [c.id for c in Comment.objects.all()])
        # self.comment_create_url = reverse('comment-list')

    def test_get_comments(self):
        self.mylogin(self.user)

        # 通过指定post_id来获取评论
        self.myheader = {'post_id' : self.post.pk}
        response = self.client.get(self.comment_create_url, self.myheader, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], self.comment.content)

        # 无指定post_id，返回全集
        response = self.client.get(self.comment_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        # post_id不存在，返回空集
        self.myheader = {'post_id' : -1}
        response = self.client.get(self.comment_create_url, self.myheader, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_comments(self):
        self.mylogin(self.user2)
        # self.myheader = {'post_id' : self.post.pk}
        data = {'content': 'New Comment', 'post_id': self.post.pk}
        response = self.client.post(self.comment_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 5)

        
        self.myheader = {'post_id' : self.post.pk}
        response = self.client.get(self.comment_create_url, self.myheader, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[1]['content'], "New Comment")
    

    def test_comment_creation_unauthenticated(self):
        # 尝试在未登录的情况下创建评论
        data = {'content': 'Unauthorized Comment', 'post_id': self.post.pk}
        response = self.client.post(self.comment_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_creation_without_content(self):
        self.mylogin(self.user2)
        data = {'post_id': self.post.pk}
        response = self.client.post(self.comment_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_own_comment(self):
        self.mylogin(self.user2)
        comment_delete_url = reverse('comment-detail', kwargs={'pk': self.comment2.pk})
        # print(Comment.objects.count())
        response = self.client.delete(comment_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_user_comment(self):
        self.mylogin(self.user3)
        comment_delete_url = reverse('comment-detail', kwargs={'pk': self.comment2.pk})
        response = self.client.delete(comment_delete_url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_single_comment(self):
        response = self.client.get(reverse('comment-detail', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.comment.pk)

    def test_update_comment(self):
        self.mylogin(self.user2)
        comment_update_url = reverse('comment-detail', kwargs={'pk': self.comment2.pk})
        data = {'content': 'Updated Comment'}
        response = self.client.put(comment_update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)





class PostLikeAPITests(APITestCase):
    def mylogin(self, user):

        self.user_data = {'username': user.username, 'code': user.openID}
        response = self.client.post('/api/v1/user/login/', self.user_data, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def getDetailPostUrl(self, pk):
        return reverse('post-detail', kwargs={'pk': pk})

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', openID = 'testopenid')
        self.user2 = User.objects.create_user(username='testuser2', openID = 'testopenid2')
        self.user3 = User.objects.create_user(username='testuser3', openID = 'testopenid3')
        self.user4 = User.objects.create_user(username='testuser4', openID = 'testopenid4')

        # 创建帖子
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.post2 = Post.objects.create(title='Test Post2', content='Test Content2', author=self.user2)
        self.post3 = Post.objects.create(title='Test Post3', content='Test Content3', author=self.user3)
        self.post4 = Post.objects.create(title='Test Post4', content='Test Content4', author=self.user4)

        # 设置 URL
        self.create_url = reverse('post-list')
        self.detail_url = reverse('post-detail', kwargs={'pk': self.post.pk})

    def test_like_post(self):
        self.mylogin(self.user2)
        response = self.client.post(reverse('post-like', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'liked')
        self.assertEqual(self.post.likes.count(), 1)
        self.assertEqual(self.post.dislikes.count(), 0)
    
    def test_dislike_post(self):
        self.mylogin(self.user2)
        response = self.client.post(reverse('post-dislike', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'disliked')
        self.assertEqual(self.post.likes.count(), 0)
        self.assertEqual(self.post.dislikes.count(), 1)

    def test_like_twice(self):
        self.mylogin(self.user2)
        response = self.client.post(reverse('post-like', kwargs={'pk': self.post.pk}))
        response = self.client.post(reverse('post-like', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'unliked')
        self.assertEqual(self.post.likes.count(), 0)
        self.assertEqual(self.post.dislikes.count(), 0)
    
    def test_dislike_twice(self):
        self.mylogin(self.user2)
        response = self.client.post(reverse('post-dislike', kwargs={'pk': self.post.pk}))
        response = self.client.post(reverse('post-dislike', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'undisliked')
        self.assertEqual(self.post.likes.count(), 0)
        self.assertEqual(self.post.dislikes.count(), 0)

    def test_like_and_dislike(self):
        self.mylogin(self.user2)
        response = self.client.post(reverse('post-like', kwargs={'pk': self.post.pk}))
        response = self.client.post(reverse('post-dislike', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'disliked')
        self.assertEqual(self.post.likes.count(), 0)
        self.assertEqual(self.post.dislikes.count(), 1)

        self.assertEqual(response.data['status'], 'disliked')
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.data['likes_count'], 0)
        self.assertEqual(response.data['dislikes_count'], 1)



class UUIDAPITests(APITestCase):
    def mylogin(self, user):

        self.user_data = {'username': user.username, 'code': user.openID}
        response = self.client.post('/api/v1/user/login/', self.user_data, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def getDetailPostUrl(self, pk):
        return reverse('post-detail', kwargs={'pk': pk})

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', openID = 'testopenid')
        self.user2 = User.objects.create_user(username='testuser2', openID = 'testopenid2')
        self.user3 = User.objects.create_user(username='testuser3', openID = 'testopenid3')
        self.user4 = User.objects.create_user(username='testuser4', openID = 'testopenid4')

        # 创建帖子
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.post2 = Post.objects.create(title='Test Post2', content='Test Content2', author=self.user2)
        self.post3 = Post.objects.create(title='Test Post3', content='Test Content3', author=self.user3)
        self.post4 = Post.objects.create(title='Test Post4', content='Test Content4', author=self.user4)

        # 设置 URL
        self.create_url = reverse('post-list')
        self.detail_url = reverse('post-detail', kwargs={'pk': self.post.pk})
    
    def test_get_uuid(self):
        self.mylogin(self.user)
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['author_uuid'], self.user.uuid)