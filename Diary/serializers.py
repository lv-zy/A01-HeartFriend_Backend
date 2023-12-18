from rest_framework import serializers
from .models import Diary, Image
from Authentication.models import User

class urlListField(serializers.ListField):
    def to_representation(self, obj):
        return obj.split(',') if obj else []
    def to_internal_value(self, data):
        return ','.join(data) if data else ''





class DiarySerializer(serializers.ModelSerializer):
    images = urlListField()
    class Meta: 
        model = Diary
        fields = '__all__'
        read_only_fields = ('id', 'author', 'create_time')

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'