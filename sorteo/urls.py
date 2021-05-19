from django.urls import path
from . import views

urlpatterns = [
    path('usuario',views.UsuarioAPIView.as_view(),name='usuario'),
    path('usuario/<int:pk>',views.UsuarioAPIView.as_view(),name='usuario'),
    path('confirm-email/<int:pk>',views.confirm_email,name='confirm-email'),
    path('create-password',views.create_password,name='change-passoword'),
    path('get-winner',views.get_winner,name='get-winner'),
]