from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.views import APIView
import zhipuai

zhipuai.api_key="f7e650710fb3e6401c689d95e0ab9fb3.eon9nUGTCXdNmWVz"

class ChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        print(request.data)
        print(data)
        response = zhipuai.model_api.invoke(
            model="chatglm_turbo",
            prompt=data,
            top_p=0.7,
            temperature=0.9,
        )
        print(response)
        if response["code"] == 200: 
            return Response(response["data"]["choices"][0], status=status.HTTP_200_OK)
        else: 
            return Response(response["msg"], status=500)

