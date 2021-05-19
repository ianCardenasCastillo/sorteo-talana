from rest_framework import serializers

from .models import *

from django.db.utils import IntegrityError


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class WinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'correo']
