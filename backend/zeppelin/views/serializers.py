from rest_framework import serializers
from django.db import models
from ..models.models import Restaurante, Usuario, CategoriaRestaurante, Direccion, Plato

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('nombre', 'apellidos', 'email', 'password', 
                  'fechaNacimiento', 'tipoUsuario') 
        extra_kwargs = {'password': {'write_only': True}}
        
class NombreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('nombre', 'apellidos')   
        
class NombreEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id','nombre', 'apellidos', 'email')                  

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ('calle', 'numero', 'ciudad', 'codigoPostal')   

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaRestaurante
        fields = '__all__'                  

class PlatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plato
        fields = '__all__'  

class RestauranteSerializer(serializers.ModelSerializer):
    direccion = DireccionSerializer()
    categorias = CategoriaSerializer(many=True)
    responsable = NombreSerializer()
    class Meta:
        model = Restaurante
        fields = '__all__'
        
class CrearRestauranteSerializer(serializers.ModelSerializer):
    direccion = DireccionSerializer()    
    class Meta:
        model = Restaurante
        fields = ('nombre', 'categorias', 'direccion')
        
    def create(self, validated_data):
        direccion_data = validated_data.pop('direccion')
        direccion = Direccion.objects.create(**direccion_data)
        restaurante = Restaurante.objects.create(direccion=direccion, **validated_data)
        return restaurante      
        
    def update(self, instance, validated_data):
        direccion_data = validated_data.pop('direccion', None)
        categorias_ids = validated_data.pop('categorias', None)
        
        if direccion_data:
            direccion_serializer = DireccionSerializer(instance.direccion, data=direccion_data, partial=True)
            if direccion_serializer.is_valid():
                direccion_serializer.save()
            else:
                raise serializers.ValidationError(direccion_serializer.errors)
        
        if categorias_ids:
            instance.categorias.set(categorias_ids)
                
        return super().update(instance, validated_data)
    