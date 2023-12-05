from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.views import APIView
from .serializers import DiarySerializer, UserDiarySerializer, ImageUploadSerializer
from .models import Diary
from .permissions import OwnerOnlyPermission
from django.conf import settings

class DiaryList(generics.ListCreateAPIView): 
    queryset = Diary.objects.filter()
    serializer_class = DiarySerializer
    permission_classes = (permissions.IsAuthenticated, OwnerOnlyPermission,)

    def get_queryset(self): 
        return Diary.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class DiaryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = (permissions.IsAuthenticated, OwnerOnlyPermission)

class ImageUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

