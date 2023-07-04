from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from datetime import datetime

from ..models.models import Restaurante, Usuario
from . import serializers

class RestauranteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RestauranteSerializer
    queryset = Restaurante.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Operación para listar los restaurantes de la base de datos",
        operation_summary="Operación para listar restaurantes",
        responses={
            200: serializers.RestauranteSerializer(many=True),
        }
    )
    def list(self, request, *args, **kwargs):
        usuario_actual = request.user

        if usuario_actual == Usuario.TipoUsuario.RESTAURANTE:
            queryset = Restaurante.objects.filter(responsable=request.user)
        else:
            queryset = Restaurante.objects.all()

        serializer = serializers.RestauranteSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Esta operación crea un restaurante",
        operation_summary="Operación para crear un nuevo Restaurante",
        request_body=serializers.CrearRestauranteSerializer,
        responses={
            201:
            openapi.Response('Restaurante creado.',
                             serializers.CrearRestauranteSerializer),
            500:
            'INTERNAL SERVER ERROR',
            400:
            'BAD REQUEST',
            405:
            'Método no permitido, tipo de usuario incorrecto'
        },
    )
    def create(self, request):
        usuario_actual = request.user
        fecha_actual = datetime.now()
        serializer = serializers.CrearRestauranteSerializer(data=request.data)
        if serializer.is_valid():
            if usuario_actual.tipoUsuario == Usuario.TipoUsuario.RESTAURANTE:
                categorias = serializer.validated_data.pop('categorias', [])
                restaurante = serializer.save(
                    fechaAlta=fecha_actual, responsable=usuario_actual)
                restaurante.categorias.set(categorias)
                return Response({'detail': 'Restaurante creado correctamente'}, status=201)
            else:
                return Response({'detail': 'Método no permitido, tipo de usuario incorrecto'}, status=405)
        else:
            return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_description="Esta operación devuelve un restaurante",
        operation_summary="Esta operación devuelve un restaurante",
    )
    def retrieve(self, request, pk=None):
        queryset = Restaurante.objects.all()
        restaurante = get_object_or_404(queryset, pk=pk)
        serializer = serializers.RestauranteSerializer(restaurante)
        ret = serializer.data
        return Response(ret)

    @swagger_auto_schema(
        operation_description='Esta operación actualiza un restaurante',
        operation_summary="Esta operación actualiza un restaurante",
        request_body=serializers.CrearRestauranteSerializer,
        responses={
            200: serializers.CrearRestauranteSerializer,
            400: 'BAD REQUEST',
            405: 'Método no permitido, tipo de usuario incorrectoo'
        },
    )
    def partial_update(self, request, pk=None):
        usuario_actual = request.user
        restaurante = get_object_or_404(self.queryset, pk=pk)
        serializer = serializers.CrearRestauranteSerializer(
            restaurante, data=request.data, partial=True)
        if (usuario_actual == restaurante.responsable):
            if serializer.is_valid():
                serializer.save()
                return Response({'detail': 'Restaurante actualizado correctamente'}, status=200)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({'detail': 'Método no permitido, usuario no dueño de restaurante'}, status=405)

    @swagger_auto_schema(
        operation_description='Esta operación elimina una categoría de restaurante',
        operation_summary="Esta operación elimina una categoría de restaurante",
        responses={
            204: 'No Content',
            404: 'Not Found',
            405: 'Método no permitido, usuario no dueño de restaurante'
        })
    def destroy(self, request, pk=None):
        usuario_actual = request.user
        restaurante = get_object_or_404(self.queryset, pk=pk)
        if (usuario_actual == restaurante.responsable):
            restaurante = get_object_or_404(self.queryset, pk=pk)
            restaurante.delete()
            return Response({'detail': 'Restaurante eliminado con exito'}, status=204)
        else:
            return Response({'detail': 'Método no permitido, usuario no dueño de restaurante'}, status=405)

    @action(detail=True, methods=['get'])
    @swagger_auto_schema(
        operation_description="Operación para listar los platos de un restaurante, si el usuario es el dueño se muestran los no validados",
        operation_summary="Operación para listar los platos de un restaurante",
        responses={
            200: serializers.PlatoSerializer(many=True),
        }
    )
    def platos(self, request, pk=None):
        restaurante = self.get_object()  # Obtener el restaurante
        usuario_actual = request.user

        # Verificar si el usuario es el dueño del restaurante
        if usuario_actual == restaurante.responsable:
            # Si es dueño, mostrar todos los platos
            queryset = restaurante.platos.all()
        else:
            # Si no es dueño, mostrar solo los platos validados
            queryset = restaurante.platos.filter(disponibilidad=True)

        serializer = serializers.PlatoSerializer(queryset, many=True)
        return Response(serializer.data)
