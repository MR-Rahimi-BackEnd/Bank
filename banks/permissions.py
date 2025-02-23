from rest_framework import permissions

class IsAdminOrOwnBank(permissions.BasePermission):
    def has_permission(self, request, view):
        
        if request.user.is_staff:
            return True  
        return False 
    def has_object_permission(self, request, view, obj):
       
        if request.user.is_staff: 
            return True
        return obj.user == request.user
    
    