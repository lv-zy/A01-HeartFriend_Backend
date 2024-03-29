from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from .utils import random_postpic_path

User = get_user_model()

class CommentStatus(models.TextChoices):
    OPEN = 'OP', 'Open for comments'
    CLOSED = 'CL', 'Closed for comments'
    AUTHORONLY = 'AU', 'Only author can comment'


class PostVisibility(models.TextChoices):
    PUBLIC = 'PU', 'Public'
    PRIVATE = 'PR', 'Private'
    # FRIENDS_ONLY = 'FO', 'Friends Only'


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='作者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='更新时间')
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True, verbose_name='点赞用户')
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True, verbose_name='踩帖用户')
    allowed_comment = models.CharField(
        max_length=2,
        choices=CommentStatus.choices,
        default=CommentStatus.OPEN
    )
    visibility = models.CharField(
        max_length=2,
        choices=PostVisibility.choices,
        default=PostVisibility.PUBLIC,
    )

    images = models.CharField(max_length=4096, default="")


    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = '帖子'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='帖子')
    content = models.TextField(verbose_name='评论内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='作者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return f"{self.author} - {self.post}"

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
    
    def save(self, *args, **kwargs):
        # 在保存评论前，更新关联帖子的更新时间
        self.post.updated_at = timezone.now()
        self.post.save()
        super().save(*args, **kwargs)

class PostImage(models.Model):
    image = models.ImageField('image', upload_to=random_postpic_path, null=True)