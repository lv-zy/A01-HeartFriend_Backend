from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import MedicineSerializer, UserMedicineSerializer
from .models import Medicine
from .permissions import OwnerOnlyPermission

class MedicineList(generics.ListCreateAPIView): 
    queryset = Medicine.objects.filter()
    serializer_class = MedicineSerializer
    permission_classes = (permissions.IsAuthenticated, OwnerOnlyPermission,)

    def get_queryset(self): 
        return Medicine.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

class MedicineDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = (permissions.IsAuthenticated, OwnerOnlyPermission)
