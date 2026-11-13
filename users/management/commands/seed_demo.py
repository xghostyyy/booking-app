from django.core.management.base import BaseCommand
from users.models import Role

class Command(BaseCommand):
    help = "Команда необходима для заполнения БД тестовыми данными"

    def handle(self, *args, **options):
        self.roles_create(name="tutor")
        self.roles_create(name="student")



    def roles_create(self, name):
        role, created = Role.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS(
            f"Роль {role} создана" if created else f"Роль {role} найдена" ))
