from django.db import models

# Create your models here.
class Widget(models.Model):
    name = models.CharField(max_length=140)

class Usuario(models.Model):
    rut = models.CharField(max_length=50)
    nombre = models.CharField(max_length=140, blank=False, null=False)
    correo = models.CharField(max_length=255, blank=False, null=False, unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    validado = models.BooleanField(blank=True, null=True, default=False)