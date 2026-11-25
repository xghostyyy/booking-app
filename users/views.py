from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from users.models import Service

@api_view(["GET"])
def service(request, service_id):
    service = get_object_or_404(Service.objects.filter(pk=service_id, is_active=True))

    return Response(
        {"message": f"Услуга: {service.title}; Исполнитель: {service.executor}; Продолжительность: {service.duration_minutes}; Цена: {service.price}; Формат: {service.format}"},
        status=200)
