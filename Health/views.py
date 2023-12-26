from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MedicineSerializer
from .models import Medicine
from .permissions import OwnerOnlyPermission
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
import requests
import json
import uuid

User = get_user_model() 

qrcode_url = "https://wxpusher.zjiecode.com/api/fun/create/qrcode"
old_app_Token = "AT_JgGxdzn8tcxvRyMsDTm33VoqAaNwLBY8"
app_Token = "AT_6HJxIZU3rx6eDm5l2zrta6IsnqoDpZZO"


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

class Qrcode(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    def post(self, request): 
        request_user = request.user
        print(f"ok Receive request from user {request_user.username}")
        response_qrcode = requests.post(qrcode_url, json={
            "appToken": app_Token, 
            "extra":str(request_user.uuid) 
        },headers={'Content-Type': 'application/json'})
        print(f"ok Post request to qrcode url")
        if (response_qrcode.status_code == 200): 
            print(f"ok get response")
            data = response_qrcode.json()
            print(data) 
            return Response(data["data"]["url"], status=200)
        else: 
            return Response({'error': 'bad request'}, status=response_qrcode.status_code)
        
class QrcodeCallback(APIView):
    permission_classes = [AllowAny]
    def post(self, request): 
        post_data = json.loads(request.body) 
        try:
            request_uuid = uuid.UUID(post_data["data"]["extra"])
            request_uid = post_data["data"]["uid"]
            subscriber = User.objects.filter(uuid=request_uuid)
            if subscriber is not None:
                subscriber.uid = request_uid
                print(f"ok record user {subscriber.uuid},  uid is {subscriber.uid}")
                return Response({'data': "received ok"}, status=200)
            else:
                print(f"unregisterd user") 
                return Response({'error': "unregistered"}, status=500)
        except:
            print(f"no bad post data")
            return Response({'error':"bad data"}, status=500)
