from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Noticia, Polo, Curso
from .forms import SearchForm, NoticiaForm, PoloForm

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

def excluir_noticia(request, noticia_id):
    if request.method == 'POST':
        noticia = get_object_or_404(Noticia, id=noticia_id)
        noticia.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

def detalhar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    dados = {
        'titulo': noticia.titulo,
        'descricao': noticia.descricao,
        'curso': noticia.curso.nome if noticia.curso else "Curso não informado",
        'publicacao': noticia.publicacao.strftime('%d/%m/%Y') if noticia.publicacao else "Data não disponível",
        'edicao': noticia.edicao.strftime('%d/%m/%Y') if noticia.edicao else "Não editado",
    }
    return JsonResponse(dados)

def editar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    
    if request.method == 'POST':
        form = NoticiaForm(request.POST, instance=noticia)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    cursos = Curso.objects.all().values('id', 'nome')
    dados = {
        'titulo': noticia.titulo,
        'descricao': noticia.descricao,
        'curso': noticia.curso.id if noticia.curso else None,
        'publicacao': noticia.publicacao.strftime('%d/%m/%Y') if noticia.publicacao else "Data não disponível",
        'edicao': noticia.edicao.strftime('%d/%m/%Y') if noticia.edicao else "Não editado",
        'cursos': list(cursos)
    }
    return JsonResponse(dados)

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
    make_polo = PoloForm(request.POST)
    search_polo = SearchForm(request.GET)
    query = request.GET.get('query')
    polos = Polo.objects.all()


    if query:
        polos = polos.filter(
            Q(cidade__icontains=query) | Q(edicao__icontains=query) | Q(publicacao__icontains=query)
        )
    
    context = {
        'make_polo': make_polo,
        'search_polo': search_polo,
        'polos': polos,
        'query': query,
    }

    return render(request, 'cead/pages/polos.html', context)

def criar_polo(request):
    if request.method == 'POST':
        form = PoloForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PoloForm()
    return render(request, 'modais_polo.html', {'form': form})

def excluir_polo(request, polo_id):
    if request.method == 'POST':
        polo = get_object_or_404(Polo, id=polo_id)
        polo.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método não permitido'})