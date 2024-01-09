#Define patrones de URL para useres.
from django.urls import path, include

app_name = 'users'
urlpatterns = [
    #Incluye url de autenticacion predeterminadas
    path('', include('django.contrib.auth.urls')),
]