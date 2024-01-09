from django.shortcuts import render, redirect
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
    # Añade tema nuevo
    if request.method != 'POST':
        # No se envían datos, crea un formulario en blanco
        form = TopicForm()
    else:
        # Datos POST enviados, procesa datos.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('app_learning_logs:topics')

    # Muestra un formulario en blanco o no válido
    context = {'form': form}
    return render(request, 'app_learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    # Añade una entrada nueva para un tema particular
    topic = Topic.objects.get(id=topic_id)

    if request.method != "POST":
        # No se han enviado datos, crea un formulario en blanco
        form = EntryForm()
    else:
        # Datos POST enviados; procesa los datos
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect("app_learning_logs:topic", topic_id=topic_id)

    # Muestra formulario en blanco o no válido
    context = {"topic": topic, "form": form}
    return render(request, "app_learning_logs/new_entry.html", context)

@login_required
def edit_entry(request, entry_id):
    #edita uan entrada existente
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    #Se aegura que solo el usuario correcta pueda acceder
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        #Solicitud inicial; prerellena el formulario con la entrada actual.
        form = EntryForm(instance=entry)
    else:
        #Datos POST enviados; procesar datos.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('app_learning_logs:topic', topic_id=topic.id)
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'app_learning_logs/edit_entry.html', context)


