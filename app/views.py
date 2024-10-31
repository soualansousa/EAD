from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Noticia

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if form.get_user().is_superuser:
                return redirect("app:home_cead")
            return redirect("app:home_coo")
    else:
        form = AuthenticationForm()
    return render(request, 'app/pages/login.html', {'form': form})

@login_required
def home_cead(request):
    return render(request, "app/pages/home_cead.html")

@login_required
def home_coo(request):
    return render(request, "app/pages/home_coo.html")

def noticias(request):
    noticias = request.GET.get(Noticia)
    return render(request, "app/pages/noticias.html", {'noticias': noticias})