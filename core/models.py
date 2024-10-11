from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, date
from multiselectfield import MultiSelectField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

######### ТИПЫ ДЛЯ CHOICES ########

class CityTypes(models.TextChoices):
    BISHKEK = 'bishkek', 'Бишкек'
    OSH = 'osh', 'Ош'
    JLD = 'jalal_abad', 'Джалал-Абад'
    
class UserTypes(models.TextChoices):
    CEO = 'ceo', 'Управляющий'
    BRANCH_SEO = 'branch_ceo', 'Управляющий филиалом'
    TEACHER = 'teacher', 'Учитель'
    ACCOUNTANT = 'accountant', 'Бухгалтер'
    EMPLOYEE = 'employee', 'Сотрудник'

class DayOfWeek(models.TextChoices):
    MONDAY = 'Понедельник', 'Понедельник'
    TUESDAY = 'Вторник', 'Вторник'
    WEDNESDAY = 'Среда', 'Среда'
    THURSDAY = 'Четверг', 'Четверг'
    FRIDAY = 'Пятница', 'Пятница'
    SATURDAY = 'Суббота', 'Суббота'
    SUNDAY = 'Воскресенье', 'Воскресенье'

class GroupStatus(models.TextChoices):
    LEARNING = 'Активна', 'Активна'
    DONE = 'Завершена', 'Завершена'
    SCHEDULED = 'Набор открыт', 'Набор открыт'

class TeacherStatus(models.TextChoices):
    FIRED = 'Уволен', 'Уволен'
    VACATION = 'На отпуске', 'На отпуске'
    WORKING = 'Работает', 'Работает'

class StudentStatus(models.TextChoices):
    STUDYING = 'Учится', 'Учится'
    VACATION = 'На отпуске', 'На отпуске'
    UNFINISHED = 'Бросил', 'Бросил'
    FINISHED = 'Закончил', 'Закончил'
    WILL_FINISH = 'Скоро закончит', 'Скоро закончит'
    PAYMENT_OVERDUE = 'Оплата просрочена', 'Оплата просрочена'

class SexTypes(models.TextChoices):
    MALE = 'Мужчина', 'Мужчина'
    FEMALE = 'Женщина', 'Женщина'

class SourceTypes(models.TextChoices):
    SOCIAL = 'Соц. сеть', 'Соц. сеть'
    FRIENDS = 'Узнал от друзей', 'Узнал от друзей'
    SAW = 'Увидел на улице', 'Увидел на улице'

####################################

class CustomUser(AbstractUser):
    type = models.CharField(
        max_length=50, 
        choices=UserTypes.choices,
        default=UserTypes.EMPLOYEE
    )
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True, blank=True)

class Branch(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=500)
    city = models.CharField(
        max_length=500, 
        choices=CityTypes.choices,
        default=CityTypes.JLD
    )

    def __str__(self):
        return f'Филиал "{self.name}" - г. {self.get_city_display()}'

class LessonSchedule(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='schedules')
    days_of_week = MultiSelectField(
        choices=DayOfWeek.choices,
        default=[DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        days_shortened = [day[:2] for day in self.days_of_week]
        days = ', '.join(days_shortened)
        return f'{days} {self.start_time.strftime("%H:%M")}-{self.end_time.strftime("%H:%M")}'
    
class WorkSchedule(models.Model):
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='work_schedules')
    days_of_week = MultiSelectField(
        choices=DayOfWeek.choices,
        default=[DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        days_shortened = [day[:2] for day in self.days_of_week]
        days = ', '.join(days_shortened)
        return f'{days} {self.start_time.strftime("%H:%M")}-{self.end_time.strftime("%H:%M")}'

class Group(models.Model):
    name = models.CharField(max_length=250, default="Группа")
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=GroupStatus.choices,
        default=GroupStatus.SCHEDULED
    )
    start_date = models.DateField() 
    duration_months = models.PositiveIntegerField()
    end_date = models.DateField(editable=False, blank=True, null=True)
    max_students = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.start_date and self.duration_months:
            self.end_date = self.start_date + timedelta(days=30 * self.duration_months)
        super().save(*args, **kwargs)

    def months_active(self):
        if self.start_date:
            return (date.today() - self.start_date).days // 30
        return 0

    def __str__(self):
        return f'Группа {self.name} в филиале {self.branch.name}'

class Teacher(models.Model):
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True, blank=True)
    sex = models.CharField(
        max_length=10,
        choices=SexTypes.choices,
        default=SexTypes.MALE
    )
    status = models.CharField(
        max_length=50,
        choices=TeacherStatus.choices,
        default=TeacherStatus.WORKING
    )
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    phone = models.CharField(max_length=30, default="+996999087108")
    whatsapp = models.CharField(max_length=30, default="+996999087108")
    description = models.TextField(max_length=1000, default="Некое описание")
    salary_rate = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    next_payment_date = models.DateField(blank=True, null=True)

    def calculate_next_payment_date(self):
        if self.start_date:
            return self.start_date + timedelta(days=30)
        return None

    def save(self, *args, **kwargs):
        # Получаем старое значение статуса для сравнения
        old_status = Teacher.objects.filter(pk=self.pk).values('status').first()
        
        # Если статус изменился с "Оплата просрочена" на "Работает"
        if old_status and old_status['status'] == TeacherStatus.FIRED and self.status == TeacherStatus.WORKING:
            self.next_payment_date = self.calculate_next_payment_date()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.surname}'


from datetime import timedelta, date

class Student(models.Model):
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True, blank=True)
    sex = models.CharField(
        max_length=10,
        choices=SexTypes.choices,
        default=SexTypes.MALE
    )
    status = models.CharField(
        max_length=50,
        choices=StudentStatus.choices,
        default=StudentStatus.STUDYING
    )
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    whatsapp = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    source = models.CharField(
        max_length=20,
        choices=SourceTypes.choices,
        default=SourceTypes.SOCIAL
    )
    payment = models.PositiveIntegerField()
    next_payment_date = models.DateField(blank=True, null=True)
    study_start_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.next_payment_date and self.study_start_date:
            self.next_payment_date = self.study_start_date + timedelta(days=30)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.surname} ({self.group.name if self.group else "No Group"})'


class FinanceRecord(models.Model):
    INCOME_TYPES = [
        ('Оплата за обучение', 'Оплата за обучение'),
        ('Авансовый платеж', 'Авансовый платеж'),
        ('Продажа учебных материалов', 'Продажа учебных материалов'),
    ]

    EXPENSE_TYPES = [
        ('Зарплата преподавателям', 'Зарплата преподавателям'),
        ('Зарплата сотруднику', 'Зарплата сотруднику'),
        ('Аренда помещения', 'Аренда помещения'),
        ('Закупка учебных материалов', 'Закупка учебных материалов'),
        ('Маркетинг и реклама', 'Маркетинг и реклама'),
        ('Операционные расходы', 'Операционные расходы'),
        ('Техническое обслуживание и IT', 'Техническое обслуживание и IT'),
        ('Покупка канцелярии', 'Покупка канцелярии'),
        ('Налоги и сборы', 'Налоги и сборы'),
    ]

    CATEGORY_CHOICES = [
        ('Доход', 'Доход'),
        ('Расход', 'Расход'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=400, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    time = models.TimeField(auto_now_add=True, blank=True, null=True)
    student = models.ForeignKey('Student', on_delete=models.SET_NULL, blank=True, null=True, related_name='finance_records')
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, blank=True, null=True, related_name='finance_records')
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, blank=True, null=True, related_name='finance_records')

    def save(self, *args, **kwargs):
        # Ограничение выбора типа в зависимости от категории
        if self.category == 'Доход' and self.type not in dict(self.INCOME_TYPES):
            raise ValueError('Некорректный тип для категории "Доход".')
        elif self.category == 'Расход' and self.type not in dict(self.EXPENSE_TYPES):
            raise ValueError('Некорректный тип для категории "Расход".')

        # Проверка привязки к модели Student или Teacher в зависимости от типа
        if self.type in ['Оплата за обучение', 'Авансовый платеж', 'Продажа учебных материалов']:
            if not self.student:
                raise ValueError('Для типа дохода, связанного со студентом, необходимо указать студента.')
        elif self.type == 'Зарплата преподавателям':
            if not self.teacher:
                raise ValueError('Для типа расхода "Зарплата преподавателям" необходимо указать преподавателя.')

        super(FinanceRecord, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.category} - {self.type} - {self.amount} - {self.date}'
    
class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(default=timezone.now)

class Attendance(models.Model):
    is_attendant = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f'{self.student} посетил {self.lesson} на {self.date}'