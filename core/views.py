from rest_framework import viewsets
from .models import CustomUser, Branch, LessonSchedule, Group, Teacher, Student, FinanceRecord, Attendance
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

class LessonScheduleViewSet(viewsets.ModelViewSet):
    queryset = LessonSchedule.objects.all()
    serializer_class = LessonScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

class WorkScheduleViewSet(viewsets.ModelViewSet):
    queryset = WorkSchedule.objects.all()
    serializer_class = WorkScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['teacher']

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('-study_start_date')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', 'branch']

    # Динамический выбор сериализатора на основе действия
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return StudentReadSerializer  # Сериализатор для чтения данных
        return StudentCreateSerializer  # Сериализатор для создания объектов

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().order_by('-start_date')
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', 'branch']

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-start_date')
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['branch']

class FinanceRecordViewSet(viewsets.ModelViewSet):
    queryset = FinanceRecord.objects.all().order_by('-date')
    serializer_class = FinanceRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['branch']

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().order_by('-date')
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'lesson']

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().order_by('-date')
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']