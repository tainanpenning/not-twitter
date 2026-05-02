from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Permission that allows only the owner of the profile to edit it, but anyone can read it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow reading for anyone
        if request.method in SAFE_METHODS:
            return True

        # Writing only allowed for the owner of the profile
        return obj.user == request.user


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Permission that allows reading for anyone,
    but only authenticated users can write.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
