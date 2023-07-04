from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404

from ..models.models import Plato, Restaurante
from . import serializers


class PlatoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlatoSerializer
    queryset = Plato.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Operación para listar los platos de la base de datos",
        operation_summary="Operación para listar todas los platos",
        responses={
            200: serializers.PlatoSerializer(many=True),
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Esta operación crea un nuevo plato",
        operation_summary="Operación para crear un plato",
        request_body=serializers.PlatoSerializer,
        responses={
            201: serializers.PlatoSerializer(),
            400: 'BAD REQUEST'
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = serializers.PlatoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_description="Esta operación devuelve un plato con un id",
        operation_summary="Esta operación devuelve un plato",
    )
    def retrieve(self, request, pk=None):
        queryset = Plato.objects.all()
        plato = get_object_or_404(queryset, pk=pk)
        serializer = serializers.PlatoSerializer(plato)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Esta operación actualiza una plato',
        operation_summary="Esta operación actualiza un plato",
        request_body=serializers.PlatoSerializer,
        responses={
            200: serializers.PlatoSerializer,
            400: 'BAD REQUEST'
        }
    )
    def partial_update(self, request, pk=None):
        plato = get_object_or_404(self.queryset, pk=pk)
        serializer = serializers.PlatoSerializer(
            plato, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_description='Esta operación elimina un plato',
        operation_summary="Esta operación elimina un plato",
        responses={
            204: 'No Content',
            404: 'Not Found'
        })
    def destroy(self, request, pk=None):
        plato = get_object_or_404(self.queryset, pk=pk)
        plato.delete()
        return Response(status=204)
