from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Noticia, Polo
from .forms import SearchForm

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if form.get_user().is_superuser:
                return redirect("cead:cead")
            return redirect("coo:coordenacao")
    else:
        form = AuthenticationForm()
    return render(request, 'cead/pages/login.html', {'form': form})

@login_required
def cead(request):
    return render(request, "cead/pages/home.html")

def noticias_lista(request):
    form = SearchForm(request.GET)
    query = request.GET.get('query')
    noticias = Noticia.objects.all()

    if query:
        noticias = noticias.filter(
            Q(titulo__icontains=query) | Q(descricao__icontains=query) | Q(edicao__icontains=query) | Q(publicacao__icontains=query) | Q(edicao__icontains=query)
        )

    context = {
        'form': form,
        'noticias': noticias
    }

    return render(request, 'cead/pages/noticias.html', context)

def polos_lista(request):
    polos = Polo.objects.all()  
    return render(request, 'cead/pages/polos.html', {'polos': polos})