from rest_framework import permissions
from django.contrib.auth.models import Group

"""A CUSTOM PERMISSION WHICH ALLOWS ONLY USERS IN ADMIN GROUP TO ACCESS DATA"""
class GroupPermission(permissions.BasePermission):
    required_groups = ['admin']

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_groups = request.user.groups.values_list('name',flat= True)
        return set(self.required_groups).issubset(user_groups)