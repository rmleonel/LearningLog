#Define patrones para learnig_log
from django.urls import path
from . import views

app_name= 'app_learning_logs'
urlpatterns = [
    #Pagina de inicio
    path('', views.index, name = 'index'),
    #Pagina que muestra todos los temas
    path('topics/', views.topics, name='topics'),
    #Pagina de detalles sobre un tema individual
    path('topics/<int:topic_id>/', views.topic, name= 'topic'),
    #Pagina para añadir un tema nuevo
    path('new_topic/', views.new_topic, name='new_topic'),
    # Pagina para añadir una entrada nueva
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # Pagina para editar una entrada
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    #Pagina para borrar un topic
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    #Pagina para borrar una entrada
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    #Pagina que me dirige a acerca de mi
    path('acerca_de_mi/', views.acerca_de_mi, name='acerca_de_mi'),
]