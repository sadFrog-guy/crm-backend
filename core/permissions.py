from rest_framework import permissions

class IsCEO(permissions.BasePermission):
    """
    Доступ только для управляющего (CEO).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.type == 'ceo'

class IsBranchManager(permissions.BasePermission):
    """
    Доступ только для управляющего филиалом (Branch Manager).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.type in ['branch_ceo', 'ceo']

    def has_object_permission(self, request, view, obj):
        if request.user.type == 'branch_ceo':
            # Проверяем, что объект принадлежит филиалу текущего пользователя
            return obj.branch == request.user.branch
        return True

class IsTeacher(permissions.BasePermission):
    """
    Доступ только для учителя.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.type == 'teacher'

    def has_object_permission(self, request, view, obj):
        if request.user.type == 'teacher':
            # Проверяем, что объект относится к группе текущего пользователя
            return obj.group in request.user.teacher.group_set.all()
        return True

class IsAuthenticatedAndOwner(permissions.BasePermission):
    """
    Доступ для аутентифицированного пользователя и владельца объекта.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user