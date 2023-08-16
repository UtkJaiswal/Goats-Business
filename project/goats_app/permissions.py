# goats_app/permissions.py

from rest_framework import permissions

class CanRetrieveUserDetails(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            if request.user.is_superuser:
                return True
            return request.user.is_authenticated
        elif request.method == 'POST':
            return True
        return False
    
class IsSellerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (user.type == 'Seller' and request.user and request.user.is_authenticated)
    

class IsAgentUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.type == 'Agent'
