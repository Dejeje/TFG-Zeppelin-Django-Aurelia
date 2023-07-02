from django.db import models
from .restaurante import Restaurante


class Plato(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    disponibilidad = models.BooleanField()
    precio = models.FloatField()
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='platos')
