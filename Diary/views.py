from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import DiarySerializer, UserDiarySerializer
from .models import Diary
from .permissions import OwnerOnlyPermission

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
