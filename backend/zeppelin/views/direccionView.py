from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from ..models.models import Direccion
from . import serializers


class DireccionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DireccionSerializer
    queryset = Direccion.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Operación para listar las direcciones de la base de datos",
        operation_summary="Operación para listar todas las direcciones",
        responses={
            200: serializers.DireccionSerializer(many=True),
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Esta operación crea una nueva dirección",
        operation_summary="Operación para crear una dirección",
        request_body=serializers.DireccionSerializer,
        responses={
            201: serializers.DireccionSerializer(),
            400: 'BAD REQUEST'
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = serializers.DireccionSerializer(
            data=request.data)
        if (serializer.is_valid()):
            direccion = serializer.save()
            direccion.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_description="Esta operación devuelve una dirección con un id",
        operation_summary="Esta operación devuelve una dirección",
    )
    def retrieve(self, request, pk=None):
        queryset = Direccion.objects.all()
        direccion = get_object_or_404(queryset, pk=pk)
        serializer = serializers.DireccionSerializer(direccion)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Esta operación actualiza una dirección',
        operation_summary="Esta operación actualiza una dirección",
        request_body=serializers.DireccionSerializer,
        responses={
            200: serializers.DireccionSerializer,
            400: 'BAD REQUEST'
        }
    )
    def partial_update(self, request, pk=None):
        direccion = get_object_or_404(self.queryset, pk=pk)
        serializer = serializers.DireccionSerializer(
            direccion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_description='Esta operación elimina una direccion',
        operation_summary="Esta operación elimina una direccion",
        responses={
            204: 'No Content',
            404: 'Not Found'
        })
    def destroy(self, request, pk=None):
        direccion = get_object_or_404(self.queryset, pk=pk)
        direccion.delete()
        return Response(status=204)
