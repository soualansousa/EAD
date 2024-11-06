from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Noticia, Polo
from .forms import SearchForm, NoticiaForm

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

def criar_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = NoticiaForm()
    return render(request, 'modais_noticia.html', {'form': form})

def noticias_lista(request):
    make_noticia = NoticiaForm(request.POST)
    search_noticia = SearchForm(request.GET)
    query = request.GET.get('query')
    noticias = Noticia.objects.all()

    if query:
        noticias = noticias.filter(
            Q(titulo__icontains=query) | Q(descricao__icontains=query) | Q(edicao__icontains=query) | Q(publicacao__icontains=query)
        )

    context = {
        'make_noticia': make_noticia,
        'search_noticia': search_noticia,
        'noticias': noticias,
        'query': query,
    }

    return render(request, 'cead/pages/noticias.html', context)

def polos_lista(request):
    form = SearchForm(request.GET)
    query = request.GET.get('query')
    polos = Polo.objects.all()

    if query:
        polos = polos.filter(
            Q(cidade__icontains=query) | Q(edicao__icontains=query) | Q(publicacao__icontains=query)
        )
    
    context = {
        'form': form,
        'polos': polos
    }

    return render(request, 'cead/pages/polos.html', context)