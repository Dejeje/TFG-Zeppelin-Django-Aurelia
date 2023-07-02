from django.db import models

class Direccion(models.Model):
    calle = models.CharField(max_length=100)
    numero = models.IntegerField()
    ciudad = models.CharField(max_length=100)
    codigoPostal = models.IntegerField()

    def __str__(self):
        return f'{self.calle}, {self.numero}, {self.ciudad}, {self.codigoPostal}'
