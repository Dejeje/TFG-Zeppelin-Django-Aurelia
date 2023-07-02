from django.db import models
from django.utils import timezone
from .restaurante import Restaurante
from .usuario import Usuario

"""
class Pedido(models.Model):
    direccion = models.CharField(max_length=100)
    fechaHora = models.DateTimeField(default=timezone.now)
    fechaEsperado = models.DateTimeField()
    comentario = models.CharField(max_length=100)
    importe = models.FloatField()
    cliente = models.ForeignKey(Usuario, related_name='pedidos_cliente', on_delete=models.CASCADE)
    repartidor = models.ForeignKey(Usuario, related_name='pedidos_repartidor', on_delete=models.CASCADE, null=True)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='pedidos')
    
"""
