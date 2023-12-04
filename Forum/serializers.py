from rest_framework import serializers
from .models import Post, Comment
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'likes_count']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'likes_count']
    
    def get_likes_count(self, obj):
        # 返回点赞的总数
        return obj.likes.count()
    


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'author', 'created_at']
        read_only_fields = ['id', 'post', 'author', 'created_at']

