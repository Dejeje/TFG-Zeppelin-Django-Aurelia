from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UsuarioManager(BaseUserManager):
    def  create_user(self, emailParam, password=None, **extra_fields):
        if not emailParam:
            raise ValueError('El email debe ser proporcionado')

        # Crear el usuario sin almacenar la contraseña directamente
        email = self.normalize_email(emailParam)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        #extra_fields.setdefault('is_staff', True)
        #extra_fields.setdefault('is_superuser', True)
        #extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('validado', 1)
        extra_fields.setdefault('tipoUsuario', 1)
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser):
    class TipoUsuario(models.IntegerChoices):
        ADMIN = 1
        RESTAURANTE = 2
        CLIENTE = 3
        RIDER = 4

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    fechaNacimiento = models.DateField(null=True)
    nombre = models.CharField(max_length=100,null=True)
    apellidos = models.CharField(max_length=100,null=True)
    validado = models.BooleanField(null=True)
    tipoUsuario = models.IntegerField(choices=TipoUsuario.choices)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'

