from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the author of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author
        return obj.author == request.user


class IsCommentAuthorOrPostAuthor(permissions.BasePermission):
    """
    Custom permission for comments:
    - Allows author to edit/delete their comment
    - Allows post author to delete comments on their post
    - Allows anyone to read
    """

    def has_permission(self, request, view):
        # Only authenticated users can create comments
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        # Read-only operations are allowed for anyone
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Edit/delete allowed for comment author or post author
        post_author = obj.post.author
        return obj.author == request.user or post_author == request.user
