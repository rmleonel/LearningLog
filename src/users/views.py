from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
# users/views.py

def register(request):
    #Registra un nuevo usuario
    if request.method != 'POST':
        #Muestra formulario de registro en blanco
        form = UserCreationForm()
    else:
        #Procesa un formulario cumplimentado
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #Inicia sesion del usuario y lo redirige a la pagina de inicio
            login(request, new_user)
            return redirect('app_learning_logs:index')
    
    #Muestra formulario en blanco no valido
    context = {'form': form}
    return render(request, 'registration/register.html', context)

@login_required
def profile(request):
    # Verifica si el perfil del usuario ya existe
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        # Procesa el formulario de perfil
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('users:profile')
    else:
        # Muestra el formulario de perfil con datos existentes si están disponibles
        form = ProfileForm(instance=profile)

    return render(request, 'registration/profile.html', {'form': form})
