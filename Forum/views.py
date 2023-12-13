from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Post, Comment, CommentStatus, PostVisibility
from .serializers import PostSerializer, CommentSerializer, postImageUploadSerializer
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.conf import settings
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
import os
from uuid import uuid4
from rest_framework.views import APIView


User = get_user_model()

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        if request.user not in post.likes.all():
            post.likes.add(request.user)
            post.dislikes.remove(request.user)  # 确保用户不能同时点赞和点踩
            return Response({"status": "liked"})
        else:
            post.likes.remove(request.user)
            return Response({"status": "unliked"})

    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        post = self.get_object()
        if request.user not in post.dislikes.all():
            post.dislikes.add(request.user)
            post.likes.remove(request.user)  # 确保用户不能同时点赞和点踩
            return Response({"status": "disliked"})
        else:
            post.dislikes.remove(request.user)
            return Response({"status": "undisliked"})
        
    @action(detail=True, methods=['post'])
    def allowComment(self, request, pk=None):
        post = self.get_object()

        if request.user != post.author:
            return Response({'message': 'You can only change your own posts.'}, status=status.HTTP_403_FORBIDDEN)

        allow_comment = request.data.get('allow_comment')
        if not allow_comment:
            return Response({"message" : "allow_comment argument not provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        if allow_comment not in CommentStatus.values:
            return Response({'message': 'Invalid comment status'}, status=status.HTTP_400_BAD_REQUEST)

        post.allowed_comment = allow_comment
        post.save()

        return Response({"allow_comment": allow_comment}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def setVisibility(self, request, pk=None):
        try:
            # 直接从Post模型获取帖子，而不是依赖get_queryset
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'message': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != post.author:
            return Response({'message': 'You can only change your own posts.'}, status=status.HTTP_403_FORBIDDEN)

        visibility = request.data.get('visibility')
        if not visibility:
            return Response({"message": "visibility argument not provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        if visibility not in PostVisibility.values:
            return Response({'message': 'Invalid visibility mode'}, status=status.HTTP_400_BAD_REQUEST)

        post.visibility = visibility
        post.save()
        return Response({"visibility": visibility}, status=status.HTTP_200_OK)

    
    
    def get_serializer_context(self):
        context = super(PostViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response({'message': 'You can only delete your own posts.'}, status=status.HTTP_403_FORBIDDEN)
        return super(PostViewSet, self).destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # 禁止更新评论
        return Response({"detail": "You are not allowed to modify posts"}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        # 禁止部分更新评论
        return Response({"detail": "You are not allowed to modify posts"}, status=status.HTTP_403_FORBIDDEN)
    
    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.all()

        public_posts = queryset.filter(visibility='PU')
        own_posts = queryset.filter(author=user)
        queryset = public_posts | own_posts
        # queryset = public_posts

        return queryset.distinct()
    

class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed or edited.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        if not post_id:
            return Response({"detail": "Post ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if post.allowed_comment == CommentStatus.CLOSED:
             return Response({"detail": "The post is not allowed to comment"}, status=status.HTTP_403_FORBIDDEN)
        elif post.allowed_comment == CommentStatus.AUTHORONLY:
            if request.user != post.author:
                return Response({"detail": "Only author can comment this post"}, status=status.HTTP_403_FORBIDDEN)
            
        

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post_id', None)
        if post_id is not None:
            queryset = queryset.filter(post__id=post_id)
            return queryset
        return Comment.objects.all()

    
    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user == comment.author:
            return super(CommentViewSet, self).destroy(request, *args, **kwargs)
        elif request.user == comment.post.author:
            return super(CommentViewSet, self).destroy(request, *args, **kwargs)

        return Response({'message': 'You can only delete your own comments.'}, status=status.HTTP_403_FORBIDDEN)


    def update(self, request, *args, **kwargs):
        # 禁止更新评论
        return Response({"detail": "You are not allowed to modify comments"}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        # 禁止部分更新评论
        return Response({"detail": "You are not allowed to modify comments"}, status=status.HTTP_403_FORBIDDEN)





class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = postImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

