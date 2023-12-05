from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    # 添加 gender 字段的选项
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('secret', 'Prefer not to say'),
    ]
    
    username = serializers.CharField(max_length=80, allow_blank=True)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    self_intro = serializers.CharField(max_length=256, allow_blank=True, required=False)
    
    avatar_url = serializers.ImageField(use_url=True, read_only=True)
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'gender', 'avatar_url', 'self_intro', 'age', 'uuid', 
                  'following_count', 'followers_count']
        read_only_fields = ('uuid', 'following_count', 'followers_count')

    def get_following_count(self, obj):
        return obj.following.count()
    
    def get_followers_count(self, obj):
        return obj.followers.count()


    def validate_username(self, value):
        """
        检查用户名长度是否合适，并且不重复。
        """
        if len(value) > 80:
            raise serializers.ValidationError("The username is too long.")

        return value

    def validate_age(self, value):
        """
        确保年龄是正整数。
        """
        if value < 0:
            raise serializers.ValidationError("Age must be a positive integer.")
        return value

    def create(self, validated_data):
        """
        禁止通过API创建新用户
        """
        raise serializers.ValidationError("Cannot create new users.")

    def update(self, instance, validated_data):
        """
        使用验证后的数据更新现有的 `User` 实例。
        """
        for field in validated_data:
            setattr(instance, field, validated_data[field])
        instance.save()
        return instance



class AvatarUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar_url']



class UserQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uuid', 'username', 'gender', 'self_intro', 'age', 'avatar_url')
        read_only_fields = ('uuid', 'username', 'gender', 'self_intro', 'age', 'avatar_url')



# 有关关注者和被关注者的序列化器
class UserBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'username', 'avatar_url', 'self_intro']

class FollowersSerializer(serializers.ModelSerializer):
    followers = UserBasicInfoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['followers']

class FollowingSerializer(serializers.ModelSerializer):
    following = UserBasicInfoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['following']