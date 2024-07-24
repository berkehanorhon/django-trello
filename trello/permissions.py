from rest_framework.permissions import BasePermission


class IsBoardMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_member(request.user)


class IsBoardAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj.is_admin(request.user))
        return obj.is_admin(request.user)
