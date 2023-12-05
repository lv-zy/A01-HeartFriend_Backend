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

class UserDiarySerializer(serializers.ModelSerializer): 
    diary_list = serializers.SerializerMethodField()
    class Meta: 
        model = User
        fields = '__all__'
    def get_diary_list(self, user):
        user_diary_list = Diary.objects.filter(author=self.context['request'].user)
        serializer = DiarySerializer(user_diary_list, many=True)
        return serializer.data
    
class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'