from users.models import Role, User, Executor, Booking, Service
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

class CatalogTest(TestCase):
    def setUp(self):
        tutor = Role.objects.create(name="tutor")
        student = Role.objects.create(name="student")
        self.ex1 = Executor.objects.create(user=User.objects.create(email="ex1@ex1.com",
            username="ex1", role=tutor))
        self.ex2 = Executor.objects.create(user=User.objects.create(email="ex2@ex2.com",
            username="ex2", role=tutor))
        self.service1 = Service.objects.create(executor=self.ex1, title="Услуга исполнителя 1",
            duration_minutes=120, price=Decimal(str(1200)), format=Service.Format.ONLINE)
        self.service2 = Service.objects.create(executor=self.ex2, title="Услуга исполнителя 2",
            duration_minutes=120, price=Decimal(str(1200)), format=Service.Format.ONLINE)
        self.user = User.objects.create(email="student@student.com",
            username="student", role=student)

    def test_booking(self):
        start = timezone.now()
        end = start + timedelta(hours=1)
        booking = Booking.objects.create(executor=self.ex1,service=self.service2,
            user=self.user, start=start, end=end)

        self.assertIsNotNone(booking.pk)

        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_protect_booking(self):
        start = timezone.now()
        end = start + timedelta(hours=1)
        booking = Booking.objects.create(executor=self.ex1, service=self.service1,
            user=self.user, start=start, end=end)

        self.assertIsNotNone(booking.pk)

        with self.assertRaises(ProtectedError):
            self.service1.delete()

        self.assertTrue(Service.objects.filter(pk=self.service1.pk).exists())
        self.assertTrue(Booking.objects.filter(pk=booking.pk).exists())
