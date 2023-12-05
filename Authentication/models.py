from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.hashers import make_password

from .utils import random_avatar_path    

class CustomUserManager(BaseUserManager):
    def create_user(self, openID, password=None, username=None, **extra_fields):
        """
        Create and return a user with an openID and optionally a username and password.
        """
        if not openID:
            raise ValueError('Users must have an openID')
        user = self.model(openID=openID, username=username, **extra_fields)
        user.password = make_password(password)  # 正确地哈希密码
        user.save(using=self._db)
        return user

    def create_superuser(self, openID, password, username=None, **extra_fields):
        """
        Create and return a superuser with admin permissions.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(openID, password, username, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('secret', 'Prefer not to say'),
    )
        
    openID = models.CharField(max_length=80, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    session_key = models.CharField(max_length=80, unique=True, null=True)
    create_time = models.IntegerField(default=int(timezone.now().timestamp()))



    username = models.CharField(max_length=80, null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='secret'
    )
    self_intro = models.CharField(max_length=256, null=True, blank=True)
    age = models.IntegerField(default=0)
    avatar_url = models.ImageField(upload_to=random_avatar_path, null=True, blank=True)




    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for admin interface
    # 注意：is_superuser 字段由 PermissionsMixin 提供

    USERNAME_FIELD = 'openID'

    objects = CustomUserManager()

    def __str__(self):
        return self.openID if not self.username else self.username

    def has_perm(self, perm, obj=None):
        # 最简单的权限策略：所有管理员拥有全部权限
        return self.is_superuser

    def has_module_perms(self, app_label):
        # 最简单的权限策略：所有管理员可以查看任何模块
        return self.is_superuser

    @property
    def is_anonymous(self):
        "Always return False. This is a way to tell if the user has been authenticated"
        return False

    @property
    def is_authenticated(self):
        "Always return True. This is a way to tell if the user has been authenticated"
        return True