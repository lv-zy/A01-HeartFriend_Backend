from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from Forum.models import Post, Comment
from .models import Report
import random

User = get_user_model()

class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.users = [
            User.objects.create_user(username=f'testuser{i}', openID=f'testopenid{i}')
            for i in range(1, 5)
        ]

        self.admin = User.objects.create_superuser(username='admin', openID='adminopenid', password='adminpassword', is_forum_admin=True)

        self.posts = []
        for user in self.users:
            for i in range(10): 
                self.posts.append(Post.objects.create(title=f'Test Post {i} by {user.username}', content=f'Test Content {i}', author=user))

        
        self.comments = []
        for post in self.posts:
            for i in range(5):  
                author = random.choice(self.users)  # 随机选择一个用户作为评论的作者

                self.comments.append(Comment.objects.create(post=post, content=f'Test Comment {i} for {post.title}', author=author))



    def mylogin(self, user):
        self.user_data = {'username': user.username, 'code': user.openID}
        response = self.client.post('/api/v1/user/login/', self.user_data, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def getDetailPostUrl(self, pk):
        return reverse('post-detail', kwargs={'pk': pk})

    def getDetailCommentUrl(self, pk):
        return reverse('comment-detail', kwargs={'pk': pk})



class ReportTest(BaseAPITestCase):

    def setUp(self):
        super().setUp()

        # 让用户3，用户4，用户5随机添加一些举报信息
        self.reports = []
        for i, post in enumerate(self.posts):
            # 随机选择一个用户作为举报者
            reporter = random.choice(self.users[2:4])
            
            # 随机选择一个举报类型
            report_types = ['spam', 'abuse', 'offensive', 'false_info', 'illegal_info', 'other']
            report_type = random.choice(report_types)

            # 创建举报
            self.reports.append(Report.objects.create(
                post=post, 
                reporter=reporter, 
                report_type=report_type, 
                details=f'Test Report {i} for {post.title}'
            ))
    
    def test_create_report(self):

        # 用户0举报多个帖子
        self.mylogin(self.users[0])

        for i in range(1, 5):
            post = self.posts[i]
            data = {'post': post.id, 'report_type': 'spam', 'details': 'test'}
            response = self.client.post(reverse('report'), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['post'], post.id)
            self.assertEqual(response.data['report_type'], 'spam')
            self.assertEqual(response.data['details'], 'test')

        response = self.client.get(reverse('user_reports'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 4)
        self.assertEqual(response.data['data'][0]['report_type'], "spam")

        # 用户1举报多个帖子
        self.mylogin(self.users[1])
        for i in range(1, 10):
            post = self.posts[i]
            data = {'post': post.id, 'report_type': 'abuse', 'details': 'test'}
            response = self.client.post(reverse('report'), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['post'], post.id)
            self.assertEqual(response.data['report_type'], 'abuse')
            self.assertEqual(response.data['details'], 'test')

        response = self.client.get(reverse('user_reports'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 9)
        self.assertEqual(response.data['data'][0]['report_type'], "abuse")


        # 不正常的参数

        # post id不存在
        self.mylogin(self.users[1])
        data = {'post': 100, 'report_type': 'abuse', 'details': 'test'}
        response = self.client.post(reverse('report'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        # 举报类型不存在或为空
        data = {'post': 1, 'report_type': 'abusee', 'details': 'test'}
        response = self.client.post(reverse('report'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'post': 1, 'details': 'test'}
        response = self.client.post(reverse('report'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 举报详情为空
        data = {'post': 1, 'report_type': 'abuse', 'details': ''}
        response = self.client.post(reverse('report'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 确保还是同样数量的举报信息
        response = self.client.get(reverse('user_reports'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 9)
        self.assertEqual(response.data['data'][0]['report_type'], "abuse")


    def test_admin_report(self):
        self.mylogin(self.admin)
        # 查看所有举报信息
        response = self.client.get(reverse('all_reports'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), len(self.reports))

        # 查看待处理的举报信息
        response = self.client.get(reverse('pending_reports'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), len(self.reports))

        
        # 处理部分举报信息
        for i in range(5):
            report = self.reports[i]
            data = {'report_status': 'accepted', 'resolution_details': 'test'}
            response = self.client.put(reverse('manage_report', kwargs={'pk': report.id}), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['report_status'], 'accepted')
            self.assertEqual(response.data['resolution_details'], 'test')

        # 部分举报信息不通过
        for i in range(5, 10):
            report = self.reports[i]
            data = {'report_status': 'rejected', 'resolution_details': 'test'}
            response = self.client.put(reverse('manage_report', kwargs={'pk': report.id}), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['report_status'], 'rejected')
            self.assertEqual(response.data['resolution_details'], 'test')
        
        # 查看待处理的举报信息
        response = self.client.get(reverse('pending_reports'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), len(self.reports) - 10)

        # 查看已处理的举报信息
        response = self.client.get(reverse('resolved_reports'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 10)


        # 用户查看自己的举报信息
        for user in [self.users[0], self.users[1]]:
            self.mylogin(user)

            # 获取该用户提交的所有举报
            response = self.client.get(reverse('user_reports'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # 从数据库获取该用户的举报记录数进行比较
            user_reports_count = Report.objects.filter(reporter=user).count()
            self.assertEqual(len(response.data['data']), user_reports_count)

            # 验证返回的举报信息确实属于该用户
            for report_data in response.data['data']:
                self.assertEqual(report_data['reporter'], user.username)

        # 管理员再次登录并验证所有举报信息的状态
        self.mylogin(self.admin)
        response = self.client.get(reverse('all_reports'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for report_data in response.data['data']:
            if report_data['id'] in [report.id for report in self.reports[:5]]:
                self.assertEqual(report_data['report_status'], 'accepted')
            elif report_data['id'] in [report.id for report in self.reports[5:10]]:
                self.assertEqual(report_data['report_status'], 'rejected')
            else:
                self.assertEqual(report_data['report_status'], 'pending')
        

    def test_create_null_post_report(self):
        self.mylogin(self.users[0])

        # 提交举报
        data = {'post': None, 'report_type': 'spam', 'details': 'test'}
        response = self.client.post(reverse('report'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'report_type': 'spam', 'details': 'test'}
        response = self.client.post(reverse('report'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'post': "wrong param",'report_type': 'spam', 'details': 'test'}
        response = self.client.post(reverse('report'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_reportExists_after_post_deletion(self):
        self.mylogin(self.admin)

        # 创建一个新帖子和新举报
        new_post = Post.objects.create(title='New Post for Report', content='Content', author=self.users[0])
        new_report = Report.objects.create(post=new_post, reporter=self.users[1], report_type='spam', details='Spam report')

        # 确保新举报已经被创建
        self.assertTrue(Report.objects.filter(id=new_report.id).exists())

        # 删除相关帖子
        response = self.client.delete(self.getDetailPostUrl(new_post.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 检查帖子是否被删除
        self.assertFalse(Post.objects.filter(id=new_post.id).exists())

        # 验证举报依然存在
        self.assertTrue(Report.objects.filter(id=new_report.id).exists())

    
    def test_get_detail_report(self):
        self.mylogin(self.users[0])

        # 创建一个新举报
        new_post = Post.objects.create(title='New Post for Report', content='Content', author=self.users[0])
        new_report = Report.objects.create(post=new_post, reporter=self.users[0], report_type='spam', details='Spam report')

        # 用户0尝试获取自己的举报信息
        response = self.client.get(reverse('single_report', kwargs={'pk': new_report.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], new_report.id)

        # 用户1尝试获取用户0的举报信息
        self.mylogin(self.users[1])
        response = self.client.get(reverse('single_report', kwargs={'pk': new_report.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 管理员尝试获取任何用户的举报信息
        self.mylogin(self.admin)
        response = self.client.get(reverse('single_report', kwargs={'pk': new_report.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], new_report.id)





    def test_User_get_feedback(self):
        self.mylogin(self.users[0])

        # 提交举报
        data = {'post': self.posts[0].id, 'report_type': 'spam', 'details': 'test'}
        response = self.client.post(reverse('report'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['post'], self.posts[0].id)
        report_id = response.data['id']

        # 查看举报列表，获取刚才那条举报，确认状态是pending
        response = self.client.get(reverse('user_reports'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['report_status'], 'pending')

        # 管理员处理举报
        self.mylogin(self.admin)
        data = {'report_status': 'accepted', 'resolution_details': 'test'}
        response = self.client.put(reverse('manage_report', kwargs={'pk': report_id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['report_status'], 'accepted')

        # 用户再次查看举报列表，发现刚才那条举报的状态不是pending了
        self.mylogin(self.users[0])
        response = self.client.get(reverse('user_reports'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['report_status'], 'accepted')

    def test_cannot_modify_twice(self):
        self.mylogin(self.users[0])

        # 提交举报
        data = {'post': self.posts[0].id, 'report_type': 'spam', 'details': 'test'}
        response = self.client.post(reverse('report'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['post'], self.posts[0].id)
        report_id = response.data['id']

        # 管理员处理举报
        self.mylogin(self.admin)
        data = {'report_status': 'accepted', 'resolution_details': 'test'}
        response = self.client.put(reverse('manage_report', kwargs={'pk': report_id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['report_status'], 'accepted')

        # 再次处理举报，应该返回400
        response = self.client.put(reverse('manage_report', kwargs={'pk': report_id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 用户再次查看举报列表，发现刚才那条举报的状态不是pending了
        self.mylogin(self.users[0])
        response = self.client.get(reverse('user_reports'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['report_status'], 'accepted')

    def test_data_struct(self):
        # 用户在提交举报后，只能看到['id', 'post', 'report_type', 'details']这几个字段
        self.mylogin(self.users[0])


class AdminDeletePostCommentTest(BaseAPITestCase):

    def setUp(self):
        super().setUp()



    def test_delete_post(self):
        self.mylogin(self.users[0])

        # 用户0删除用户1的帖子，应该返回403
        response = self.client.delete(self.getDetailPostUrl(self.posts[10].id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 用户0删除自己的帖子，应该返回204
        response = self.client.delete(self.getDetailPostUrl(self.posts[0].id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 用户0删除自己的帖子，应该返回404
        response = self.client.delete(self.getDetailPostUrl(self.posts[0].id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


        # 管理员删除用户1的帖子，应该返回204
        self.mylogin(self.admin)
        response = self.client.delete(self.getDetailPostUrl(self.posts[10].id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


        # 管理员删除不存在的帖子，应该返回404
        response = self.client.delete(self.getDetailPostUrl(self.posts[0].id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment(self):
        # 用户0尝试删除不属于自己的评论，应返回403
        self.mylogin(self.users[0])
        other_user_comment = next(c for c in self.comments if c.author != self.users[0] and c.post.author != self.users[0])
        response = self.client.delete(self.getDetailCommentUrl(other_user_comment.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 用户0删除自己的评论，应返回204
        own_comment = next(c for c in self.comments if c.author == self.users[0])
        response = self.client.delete(self.getDetailCommentUrl(own_comment.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 用户0尝试再次删除同一个评论，应返回404
        response = self.client.delete(self.getDetailCommentUrl(own_comment.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # 管理员尝试删除其他用户的评论，应返回204
        self.mylogin(self.admin)
        another_user_comment = next(c for c in self.comments if c.author != self.admin)
        response = self.client.delete(self.getDetailCommentUrl(another_user_comment.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 管理员尝试删除一个不存在的评论，应返回404
        non_existing_comment_id = 99999  # 假设的不存在的评论ID
        response = self.client.delete(self.getDetailCommentUrl(non_existing_comment_id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


  