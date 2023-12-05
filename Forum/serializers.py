from rest_framework import serializers
from .models import Post, Comment, PostImage
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    author_uuid = serializers.ReadOnlyField(source='author.uuid')

    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()

    comments_count = serializers.SerializerMethodField()

    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 
                  'likes_count', 'is_liked', 'dislikes_count', 'is_disliked', 'comments_count', 
                  'author_uuid',
                  'is_following',
                  'images'
                  ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 
                            'likes_count', 'is_liked', 'comments_count', 'dislikes_count', 'is_disliked', 
                            'author_uuid',
                            'is_following'
                            ]
    
    def get_likes_count(self, obj):
        # 返回点赞的总数
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return obj.likes.filter(id=request.user.id).exists()
        return False
    
    def get_dislikes_count(self, obj):
        # 返回点赞的总数
        return obj.dislikes.count()
    
    def get_is_disliked(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return obj.dislikes.filter(id=request.user.id).exists()
        return False

    def get_comments_count(self, obj):
        # 返回评论的总数
        return obj.comments.count()
    
    def get_author_uuid(self, obj):
        return obj.author.uuid
    
    def get_is_following(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return request.user.is_following(obj.author)
        return False


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_uuid = serializers.ReadOnlyField(source='author.uuid')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'author', 'created_at', 'author_uuid']
        read_only_fields = ['id', 'post', 'author', 'created_at', 'author_uuid']

    def get_author_uuid(self, obj):
        return obj.author.uuid



class postImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'
