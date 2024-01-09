#Define patrones de URL para users.
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'users'
urlpatterns = [
    #Incluye url de autenticacion predeterminadas
    path('', include('django.contrib.auth.urls')),
    # Pagina de registro
    path('register/', views.register, name='register'),
    #Pagina de confirmacion de sesion cerrada
    path('logout/', LogoutView.as_view(), name='logout'),
]