from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return str(self.name)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="users",
        null=True,
        blank=True)

    def __str__(self):
        return str(self.email)

class Executor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
        related_name="executor_profile")
    specialization = models.CharField(max_length=50, null=False)
    bio = models.TextField(blank=True)

    def __str__(self):
        return str(f"Специализация: {self.specialization}")

class Service(models.Model):
    executor = models.ForeignKey(Executor, on_delete=models.CASCADE,
        related_name="services")
    title = models.CharField(max_length=50)
    duration_minutes = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Format(models.TextChoices):
        OFFLINE = "offline", "Офлайн"
        ONLINE = "online", "Онлайн"

    format = models.CharField(max_length=10, choices=Format.choices)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(f"Услуга: {self.title}")

class WorkingHours(models.Model):
    executor = models.ForeignKey(Executor, on_delete=models.CASCADE,
        related_name="working_hours")

    class Weekdays(models.IntegerChoices):
        Monday = 0, "Понедельник"
        Tuesday = 1, "Вторник"
        Wednesday = 2, "Среда"
        Thursday = 3, "Четверг"
        Friday = 4, "Пятница"
        Saturday = 5, "Суббота"
        Sunday = 6, "Воскресенье"

    weekday = models.PositiveSmallIntegerField(choices=Weekdays.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering= ["weekday", "start_time"]
        constraints = [
            models.UniqueConstraint(fields=["executor", "weekday", "start_time"],
                name="unique_working_hours_slot"),
            models.CheckConstraint(
                condition=models.Q(start_time__lt=models.F("end_time")),
                name="working_hours_start_before_end",
            )
        ]

    def __str__(self):
        return str(f"Рабочие часы: с {self.start_time} до {self.end_time} по {self.weekday}")

class TimeOff(models.Model):
    executor = models.ForeignKey(Executor, on_delete=models.CASCADE,
        related_name="time_offs")
    start = models.DateTimeField()
    end = models.DateTimeField()
    reason = models.CharField(blank=True, max_length=50)

    class Meta:
        ordering = ["start", "end"]

    def __str__(self):
        return str(f"Начало: {self.start}, Конец: {self.end}, Примечание: {self.reason}")

class Booking(models.Model):
    executor = models.ForeignKey(Executor, on_delete=models.PROTECT,
        related_name="bookings")
    service = models.ForeignKey(Service, on_delete=models.PROTECT,
        related_name="bookings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT,
        related_name="bookings")
    start = models.DateTimeField()
    end = models.DateTimeField()

    class STATUS(models.TextChoices):
        PENDING = "pending", "В ожидании",
        CONFIRMED = "confirmed", "Подтвержден",
        CANCELLED = "cancelled", "Отклонен",
        COMPLETED = "completed", "Завершен"

    status = models.CharField(choices=STATUS.choices, default=STATUS.PENDING, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.service_id or not self.executor_id:
            return
        if self.service.executor_id != self.executor_id:
            raise ValidationError("Услуга принадлежит другому исполнителю")

    class Meta:
        ordering = ["-start"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(start__lt=models.F("end")),
                name="booking_start_before_end",
            )
        ]

    def __str__(self):
        return str(f"{self.start} - {self.end}, статус: {self.status}, создано: {self.created_at}")
