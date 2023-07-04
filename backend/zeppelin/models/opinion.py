from django.db import models
from .restaurante import Restaurante
from .usuario import Usuario

class Opinion(models.Model):
    opinion = models.CharField(max_length=100)
    valor = models.FloatField()
#    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='opiniones')
#    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='opiniones')
    
    def __str__(self):
        return self.opinion