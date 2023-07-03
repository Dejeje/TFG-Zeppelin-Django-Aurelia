from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import login, logout

from django.shortcuts import get_object_or_404

from django.db.models import Q
from ..models.models import Usuario
from . import serializers

@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        operation_description="Esta operación lista los usuarios disponibles",
        operation_summary="Operación para listar usuarios",
        responses={
            201: serializers.UsuarioSerializer(many=True),
        }
    ))
class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UsuarioSerializer
    queryset = Usuario.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    @swagger_auto_schema(
        operation_description="Esta operación devuelve el usuario actualmente autenticado",
        operation_summary="Obtener usuario actual",
        responses={
            200: serializers.UsuarioSerializer(),
            403: 'No hay usuario autenticado',
        },
    )    
    def perfil(self, request):
        if request.user.is_authenticated:
            usuario = request.user
            serializer = self.get_serializer(usuario)
            return Response(serializer.data)
        else:
             return Response({'detail': 'No hay usuario autenticado'}, status=403)
         
    @swagger_auto_schema(
        operation_description="Esta operación crea un usuario",
        operation_summary="Operación para crear un nuevo Usuario",
        request_body=serializers.RegistroSerializer,
        responses={
            201:
            openapi.Response('Usuario registrado correctamente.',
                             serializers.UsuarioSerializer),
            400: 'El email ya está registrado',
            401: 'Registro incorrecto'
        })
    def create(self, request):
        serializer = serializers.RegistroSerializer(data=request.data)
        if serializer.is_valid():

            tipo_usuario = serializer.validated_data.get('tipoUsuario')
            usuario = serializer.save()

            # Definir validado según el tipo de usuario
            usuario.validado = (tipo_usuario == Usuario.TipoUsuario.CLIENTE)

            # Encriptar la contraseña
            usuario.password = make_password(usuario.password)
            usuario.save()
              
            if usuario is not None:
                # El usuario ha sido creado correctamente
                return Response({'detail': 'Registro exitoso'}, status=201)
            else:
                return Response({'detail': 'Registro incorrecto'}, status=401)
           
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_description="Esta operación logea a un usuario",
        operation_summary="Operación para hacer login a un Usuario",
        request_body=serializers.LoginSerializer,
        responses={
            200: 'Inicio de sesión exitoso',
            401: 'Credenciales inválidas',
        }
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            try:
                usuario = Usuario.objects.get(email=email)
            except BaseException as e:
                return Response({'detail': 'Email no existe'}, status=401)

            if not check_password(password, usuario.password):
                return Response({'detail': 'Credenciales inválidas'}, status=401)

            if not usuario.validado:
                return Response({'detail': 'Usuario no validado'}, status=401)
            
            token = Token.objects.get_or_create(user=usuario)[0].key
            login(request, usuario)
            
            return Response({'detail': 'Inicio de sesión exitoso', 'access_token': token})

        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(
        operation_description="Esta operación cierra la sesión de un usuario",
        operation_summary="Operación para cierrar la sesión de un usuario",
        responses={
            200: 'Cierre de sesión exitoso',
        },
    )
    def logout(self, request):
        if request.user.is_authenticated:
            if request.user.auth_token:
                request.user.auth_token.delete()
            logout(request)
            return Response({'detail': 'Cierre de sesión exitoso'}, status=200)
        else:
             return Response({'detail': 'No hay usuario autenticado'}, status=403)

    @action(detail=False, methods=['get'], url_path='validar/(?P<id>[^/.]+)')
    @swagger_auto_schema(
        operation_description="Esta operación valida un usuario de tipo restaurante, solo por el admin",
        operation_summary="Esta operación valida un usuario de tipo restaurante",
        responses={
            200: 'Usuario validado',
            401: 'No tienes autorizacion',
            403: 'No hay usuario autenticado',
        },
    )    
    def validar(self, request,id=None):
        if request.user.is_authenticated:
            usuario = request.user
            if usuario.tipoUsuario == Usuario.TipoUsuario.ADMIN:
                 
                user = get_object_or_404(self.queryset, pk=id)
                user.validado = True
                user.save()
                
                return Response({'detail': 'Usuario con ID ' + id + ' validado'}, status=200)
            else:
                return Response({'detail': 'No tienes permisos'}, status=401)
        else:
             return Response({'detail': 'No hay usuario autenticado'}, status=403)
         
    @action(detail=False, methods=['get'])
    @swagger_auto_schema(
        operation_description="Esta operación devuelve el listado de usuario por validar",
        operation_summary="Obtener listado de usuario por validar",
        responses={
            200: serializers.NombreEmailSerializer(),
            403: 'No hay usuario autenticado',
        },
    )    
    def por_validar(self, request):
        if request.user.is_authenticated:
            usuarios = Usuario.objects.filter(Q(validado=False) & Q(tipoUsuario=Usuario.TipoUsuario.RESTAURANTE))
            serializer = serializers.NombreEmailSerializer(usuarios, many=True)
            return Response(serializer.data, status=200)
        else:
             return Response({'detail': 'No hay usuario autenticado'}, status=403)