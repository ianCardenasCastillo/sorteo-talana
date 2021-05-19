from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from . import models  # Se importan los modelos
# Se importan los serializers (combierten el queryset en Json)
from . import serializers

from .tasks import send_email

# Create your views here.


class UsuarioAPIView(APIView):
    """
    Función para obtener un usuario
    Recive como parametro un correo
    Si existe un usuario con el correo devuelve el usuario
    de lo contrario retornara None
    """

    def get_user_by_email(self, correo):
        try:
            return models.Usuario.objects.get(correo=correo)
        except models.Usuario.DoesNotExist:
            return None

    def get_user_by_pk(self, pk):
        try:
            return models.Usuario.objects.get(pk=pk)
        except models.Usuario.DoesNotExist:
            return None

    def get(self, request, pk=None):
        if pk is None:
            return Response({"pk": ["Falta el pk del usuario a buscar"]}, status=status.HTTP_400_BAD_REQUEST)
        usuario = self.get_user_by_pk(pk)
        if usuario is None:
            return Response({"message": "No se encontro el Usuario"}, status=status.HTTP_204_NO_CONTENT)
        serializer = serializers.UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = None
        if "multipart/form-data" in request.content_type:
            data = request.data
            data = json.loads(data)
        if "application/json" in request.content_type:
            data = request.data
        serializer = serializers.UsuarioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            send_email.delay(serializer.data.get(
                'correo'), serializer.data.get('id'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk=None):
        if pk is None:
            return Response({"pk": ["Falta el pk del objeto a eliminar"]}, status=status.HTTP_400_BAD_REQUEST)
        usuario = self.get_user_by_pk(pk)
        if usuario is None:
            return Response({"message": "No se encontro el Usuario"}, status=status.HTTP_204_NO_CONTENT)
        usuario.delete()
        return Response({"message": "Usurio Eliminado"}, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def confirm_email(request, pk):
    def get_user_by_pk(pk):
        try:
            return models.Usuario.objects.get(pk=pk)
        except models.Usuario.DoesNotExist:
            return None
    if pk is None:
        return Response({"pk": ["Falta el pk del usuario a confirmar"]}, status=status.HTTP_400_BAD_REQUEST)
    usuario = get_user_by_pk(pk)
    if usuario is None:
        return Response({"msg": "No se encontro el Usuario"}, status=status.HTTP_204_NO_CONTENT)
    if usuario.validado:
        return Response("Correo ya se encuentra validado", status=status.HTTP_200_OK)
    usuario.validado = True
    usuario.save()
    return Response("Confirmado Correctamente", status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
def create_password(request):
    def get_user_by_pk(pk):
        try:
            return models.Usuario.objects.get(pk=pk)
        except models.Usuario.DoesNotExist:
            return None
    data = None
    if "multipart/form-data" in request.content_type:
        data = request.data
        data = json.loads(data)
    if "application/json" in request.content_type:
        data = request.data
    usuario = get_user_by_pk(data.get('id'))
    if usuario is None:
        return Response({"message": "No se encontro el Usuario"}, status=status.HTTP_204_NO_CONTENT)
    if usuario.validado:
        if usuario.password:
            return Response({"msg": "Ya cuenta con una contraseña"}, status=status.HTTP_200_OK)
        usuario.password = data.get('password')
        usuario.save()
        return Response({"msg": "Contraseña Creada"}, status=status.HTTP_200_OK)
    return Response({"msg": "Primero debe confirmar su correo"}, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def get_winner(request):
    def get_random_user():
        try:
            return models.Usuario.objects.filter(validado=True, password__isnull=False).order_by('?')[0]
        except models.Usuario.DoesNotExist:
            return None
        except IndexError:
            return None
    user = get_random_user()
    if user:
        serializer = serializers.WinnerSerializer(user)
        return Response({"ganador": serializer.data}, status=status.HTTP_200_OK)
    return Response({"msg": "No existen usuarios validos en el sorteo"}, status=status.HTTP_204_NO_CONTENT)
