from django.core.management.base import BaseCommand
from users.models import Role, User, Executor, Service, WorkingHours
from decimal import Decimal
from datetime import time

class Command(BaseCommand):
    help = "Команда необходима для заполнения БД тестовыми данными"

    def handle(self, *args, **options):
        self.roles(name="tutor")
        self.roles(name="student")
        self.user(email="student@student.com", role="student")

        tutor_user = self.user(email="tutor@tutor.com", role="tutor")
        tutor_executor = self.executor(user=tutor_user)

        self.service(executor=tutor_executor, title="Математика 90 минут",
            duration_minutes=90, price=1000, format=Service.Format.OFFLINE)
        self.service(executor=tutor_executor, title="Геометрия 60 минут",
            duration_minutes=60, price=8000, format=Service.Format.ONLINE)
        self.working_hours(executor=tutor_executor, weekday=WorkingHours.Weekdays.Monday,
            start_time=time(10,0), end_time=time(18,0))
        self.working_hours(executor=tutor_executor, weekday=WorkingHours.Weekdays.Tuesday,
            start_time=time(12,0), end_time=time(20,0))


    def roles(self, name):
        role, created = Role.objects.get_or_create(name=name)

        self.stdout.write(self.style.SUCCESS(
            f"Роль {role} " + ("coздана." if created else "найдена.")
        ))

    def user(self, email, role):
        DEMO_PASSWORD = "pass123"

        role_obj = Role.objects.get(name=role)
        defaults={"username": str(role_obj), "role": role_obj}

        user, created = User.objects.get_or_create(email=email, defaults=defaults)
        if created:
            user.set_password(DEMO_PASSWORD)
            user.save()

        self.stdout.write(self.style.SUCCESS(
            f"Пользователь {email} " + ("coздан." if created else "найден.")
        ))

        return user

    def executor(self, user):
        defaults = {"specialization": "Math"}
        executor, created = Executor.objects.get_or_create(user=user, defaults=defaults)

        self.stdout.write(self.style.SUCCESS(
            f"Исполнитель {user.email} " + ("coздан." if created else "найден.")
        ))

        return executor

    def service(self, executor, title, duration_minutes, price, format):
        defaults = {"duration_minutes": duration_minutes, "price": Decimal(str(price)), "format": format}

        service, created = Service.objects.get_or_create(executor=executor, title=title, defaults=defaults)

        self.stdout.write(self.style.SUCCESS(
            f"Услуга {title} " + ("coздана." if created else "найдена.")
        ))

    def working_hours(self, executor, weekday, start_time, end_time):
        defaults = {"end_time": end_time}

        wh, created = WorkingHours.objects.get_or_create(executor=executor, weekday=weekday, start_time=start_time, defaults=defaults)

        self.stdout.write(self.style.SUCCESS(
            f"Рабочие часы {wh.get_weekday_display()} {wh.start_time:%H:%M}-{wh.end_time:%H:%M} " + ("coзданы." if created else "найдены.")
        ))
