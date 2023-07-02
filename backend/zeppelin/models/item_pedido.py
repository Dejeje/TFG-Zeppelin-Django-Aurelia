from django.db import models
from .pedido import Pedido
from .plato import Plato
"""
class ItemPedido(models.Model):
    cantidad = models.IntegerField()
    precioTotal = models.FloatField()
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='item_pedidos')
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)

    def __str__(self):
        return self.cantidad
"""
