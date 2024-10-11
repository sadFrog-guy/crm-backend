from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'branches', views.BranchViewSet)
router.register(r'lesson-schedules', views.LessonScheduleViewSet)
router.register(r'work-schedules', views.WorkScheduleViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'teachers', views.TeacherViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'finance-records', views.FinanceRecordViewSet)
router.register(r'attendances', views.AttendanceViewSet)
router.register(r'lessons', views.LessonViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Включаем маршруты от роутера

    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Логин, получение токена
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена
]
