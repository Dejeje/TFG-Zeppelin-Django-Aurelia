from django.db import models

class CategoriaRestaurante(models.Model):
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.categoria
