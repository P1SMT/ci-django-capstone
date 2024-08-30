from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CityForm, UserRegisterForm
from .models import City

@login_required
def index(request):
    cities = City.objects.filter(user=request.user)
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.save(commit=False)
            city.user = request.user
            city.save()
            messages.success(request, f'City {city.name} added to your favorites.')
            return redirect('index')
    else:
        form = CityForm()

    context = {'cities': cities, 'form': form}
    return render(request, 'weather/index.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('index')
    else:
        form = UserRegisterForm()

    return render(request, 'weather/register.html', {'form': form})

@login_required
def delete_city(request, city_id):
    city = City.objects.get(id=city_id)
    if city.user == request.user:
        city.delete()
        messages.success(request, f'City {city.name} has been deleted.')
    return redirect('index')
