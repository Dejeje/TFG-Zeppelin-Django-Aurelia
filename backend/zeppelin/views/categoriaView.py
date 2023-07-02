from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from ..models.models import CategoriaRestaurante
from . import serializers


class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategoriaSerializer
    queryset = CategoriaRestaurante.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Operación para listar las categorias de restaurantes de la base de datos",
        operation_summary="Operación para listar las categorias de restaurantes",
        responses={
            200: serializers.CategoriaSerializer(many=True),
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Esta operación crea una categoria de restaurante",
        operation_summary="Operación para crear una nueva categoria de Restaurante",
        request_body=serializers.CategoriaSerializer,
        responses={
            201: serializers.CategoriaSerializer(),
            400: 'BAD REQUEST'
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = serializers.CategoriaSerializer(
            data=request.data)
        if (serializer.is_valid()):
            categoria = serializer.save()
            categoria.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_description="Esta operación devuelve una categoria de restaurante",
        operation_summary="Esta operación devuelve una categoria de restaurante",
    )
    def retrieve(self, request, pk=None):
        queryset = CategoriaRestaurante.objects.all()
        categoria = get_object_or_404(queryset, pk=pk)
        serializer = serializers.CategoriaSerializer(categoria)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Esta operación actualiza una categoria de restaurante',
        operation_summary="Esta operación actualiza una categoria de restaurante",
        request_body=serializers.CategoriaSerializer,
        responses={
            200: serializers.CategoriaSerializer,
            400: 'BAD REQUEST'
        }
    )
    def partial_update(self, request, pk=None):
        categoria = get_object_or_404(self.queryset, pk=pk)
        serializer = serializers.CategoriaRestauranteSerializer(
            categoria, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_description='Esta operación elimina una categoría de restaurante',
        operation_summary="Esta operación elimina una categoría de restaurante",
        responses={
            204: 'No Content',
            404: 'Not Found'
        })
    def destroy(self, request, pk=None):
        categoria = get_object_or_404(self.queryset, pk=pk)
        categoria.delete()
        return Response(status=204)
