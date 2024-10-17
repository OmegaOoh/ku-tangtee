from rest_framework import permissions


class IsHostOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # GET, HEAD or OPTIONS requests are allowed.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Edit permissions are only allowed to the host.
        return request.user == obj.host()
