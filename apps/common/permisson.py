from rest_framework import permissions



class CanWriteReview(permissions.BasePermission):

    def has_permission(self, request, view):
        return  request.user and request.user.verified


from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Faqat admin foydalanuvchilarga ruxsat beruvchi permission.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff  # Faqat adminlarga ruxsat
