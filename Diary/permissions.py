# Diary/permissions.py
from rest_framework import permissions

class OwnerOnlyPermission(permissions.BasePermission):
    """
    自定义权限只允许对象的创建者获取、修改、删除对象
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
