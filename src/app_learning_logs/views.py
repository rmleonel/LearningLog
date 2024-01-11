from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm 

def index(request):
    #Pagina de inicio
    return render(request, "app_learning_logs/index.html")

@login_required
def topics(request):
    #Muestra todos los temas
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'app_learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    #Muestra un tema concreto y todas sus entradas
    topic = Topic.objects.get(id=topic_id)
    # Se asegura de que el tema pertenece al usuario actual
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render (request, 'app_learning_logs/topic.html', context)

@login_required
def new_topic(request):
    # Añade un tema nuevo
    if request.method == 'POST':
        if 'cancel' in request.POST:
            # Si se presiona el botón de cancelar, redirige a otra página
            return redirect('app_learning_logs:topics')

        # Datos POST enviados, procesa datos.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('app_learning_logs:topics')
    else:
        # No se envían datos, crea un formulario en blanco
        form = TopicForm()

    # Muestra un formulario en blanco o no válido
    context = {'form': form}
    return render(request, 'app_learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    # Añade una entrada nueva para un tema particular
    topic = Topic.objects.get(id=topic_id)

    if request.method == "POST":
        if 'cancel' in request.POST:
            # Si se presiona el botón de cancelar, redirige a otra página
            return redirect("otra_pagina")

        # Datos POST enviados; procesa los datos
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect("app_learning_logs:topic", topic_id=topic_id)
    else:
        # No se han enviado datos, crea un formulario en blanco
        form = EntryForm()

    # Muestra formulario en blanco o no válido
    context = {"topic": topic, "form": form}
    return render(request, "app_learning_logs/new_entry.html", context)

@login_required
def edit_entry(request, entry_id):
    # Obtiene la entrada existente que se va a editar según el ID proporcionado.
    entry = Entry.objects.get(id=entry_id)
    
    # Obtiene el tema asociado con la entrada.
    topic = entry.topic
    
    # Asegura que solo el usuario correcto pueda acceder a la edición de la entrada.
    if topic.owner != request.user:
        raise Http404
    
    if request.method == 'POST':
        # Datos POST enviados; procesa los datos del formulario.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            # Si el formulario es válido, guarda la entrada editada y redirige al detalle del tema.
            form.save()
            return redirect('app_learning_logs:topic', topic_id=topic.id)
    else:
        # Solicitud GET; prerrellena el formulario con la entrada actual.
        form = EntryForm(instance=entry)
    
    # Crea un contexto con la entrada, el tema y el formulario para pasar a la plantilla.
    context = {'entry': entry, 'topic': topic, 'form': form}
    
    return render(request, 'app_learning_logs/edit_entry.html', context)

def delete_entry(request, entry_id):
    # Obtiene la entrada que se va a eliminar según el ID proporcionado.
    entry = get_object_or_404(Entry, id=entry_id)
    
    # Obtiene el tema asociado con la entrada.
    topic = entry.topic
    
    # Asegura que solo el usuario correcto pueda acceder a la eliminación de la entrada.
    if topic.owner != request.user:
        raise Http404
    
    if request.method == 'POST':
        # Confirma que la solicitud es mediante el método POST.
        entry.delete()
        return redirect('app_learning_logs:topic', topic_id=topic.id)
    
    # Si la solicitud no es mediante el método POST, renderiza el formulario de confirmación de eliminación.
    context = {'entry': entry, 'topic': topic}
    return render(request, 'app_learning_logs/delete_entry.html', context)

