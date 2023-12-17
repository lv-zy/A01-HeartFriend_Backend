from rest_framework import permissions


class IsForumAdmin(permissions.BasePermission):
    """
    论坛管理员权限
    """
    def has_permission(self, request, view):
        return request.user.is_forum_admin

