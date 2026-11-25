from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from users.models import Service
from users.serializers import ServiceSerializer

@api_view(["GET"])
def service(request, service_id):
    service = get_object_or_404(Service.objects.filter(pk=service_id, is_active=True))
    serializer = ServiceSerializer(service)

    return Response(serializer.data, status=200)

@api_view(["GET"])
def services(request):
    qs = Service.objects.filter(is_active=True)

    return Response(ServiceSerializer(qs, many=True).data, status=200)
