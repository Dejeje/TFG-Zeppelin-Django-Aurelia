from django.db import models
from .categoria_restaurante import CategoriaRestaurante
from .direccion import Direccion
from .usuario import Usuario

class Restaurante(models.Model):
    nombre = models.CharField(max_length=100)
    fechaAlta = models.DateField()
    categorias = models.ManyToManyField(CategoriaRestaurante)
    direccion = models.OneToOneField(Direccion, on_delete=models.CASCADE)
    responsable = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='restaurantes')

    def __str__(self):
        return f"Restaurante: {self.nombre}\nID: {self.id}\nFecha de Alta: {self.fechaAlta}\nValoración Global: {self.valoracionGlobal}\nNúmero de Valoraciones: {self.numValoraciones}\nNúmero de Penalizaciones: {self.numPenalizaciones}"
 