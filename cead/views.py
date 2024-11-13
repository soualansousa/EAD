from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Noticia, Polo, Curso, Coordenador
from .forms import SearchForm, NoticiaForm, PoloForm, CoordenadorForm, CursoForm

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

# polo

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

def detalhar_polo(request, polo_id):
    polo = get_object_or_404(Polo, id=polo_id)
    dados = {
        'cidade': polo.cidade,
        'latitude': polo.latitude,
        'longitude': polo.longitude,
        'coordenador': polo.coordenador.nome if polo.coordenador else "Coordenador não informado",
        'publicacao': polo.publicacao.strftime('%d/%m/%Y') if polo.publicacao else "Data não disponível",
        'edicao': polo.edicao.strftime('%d/%m/%Y') if polo.edicao else "Não editado",
    }
    return JsonResponse(dados)

def editar_polo(request, polo_id):
    polo = get_object_or_404(Polo, id=polo_id)
    
    if request.method == 'POST':
        form = PoloForm(request.POST, instance=polo)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    coordenadores = Coordenador.objects.all().values('id', 'nome')
    dados = {
        'cidade': polo.cidade,
        'latitude': polo.latitude,
        'longitude': polo.longitude,
        'coordenador': polo.coordenador.id if polo.coordenador else None,
        'publicacao': polo.publicacao.strftime('%d/%m/%Y') if polo.publicacao else "Data não disponível",
        'edicao': polo.edicao.strftime('%d/%m/%Y') if polo.edicao else "Não editado",
        'coordenadores': list(coordenadores)
    }
    return JsonResponse(dados)

# coordenador

def coordenadores_lista(request):
    make_coordenador = CoordenadorForm(request.POST)
    search_coordenador = SearchForm(request.GET)
    query = request.GET.get('query')
    coordenadores = Coordenador.objects.all()


    if query:
        coordenadores = coordenadores.filter(
        Q(situacao__icontains=query) |
        Q(edicao__icontains=query) |
        Q(publicacao__icontains=query) |
        Q(nome__icontains=query) |
        Q(telefone__icontains=query) |
        Q(email__icontains=query)
        )
    
    context = {
        'make_coordenador': make_coordenador,
        'search_coordenador': search_coordenador,
        'coordenadores': coordenadores,
        'query': query,
    }

    return render(request, 'cead/pages/coordenadores.html', context)


def criar_coordenador(request):
    if request.method == 'POST':
        form = CoordenadorForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CoordenadorForm()
    return render(request, 'modais_coordenadores.html', {'form': form})


def detalhar_coordenador(request, coordenador_id):
    coordenador = get_object_or_404(Coordenador, id=coordenador_id)
    dados = {
        'nome': coordenador.nome,
        'email': coordenador.email,
        'telefone': coordenador.telefone,
        'situacao': "Ativo" if coordenador.situacao else "Inativo",
        'publicacao': coordenador.publicacao.strftime('%d/%m/%Y') if coordenador.publicacao else "Data não disponível",
        'edicao': coordenador.edicao.strftime('%d/%m/%Y') if coordenador.edicao else "Não editado",
    }
    return JsonResponse(dados)
 

def editar_coordenador(request, coordenador_id):
    coordenador = get_object_or_404(Coordenador, id=coordenador_id)
    
    if request.method == 'POST':
        # if request.method == 'POST':
            
        #     situacao = request.POST.get('situacao') 

        coordenador.situacao = request.POST.get('situacao')
        coordenador.nome = request.POST.get('nome')
        coordenador.email = request.POST.get('email')
        coordenador.telefone = request.POST.get('telefone')

        coordenador.save()


            # form.save()
        return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    # coordenadores = Coordenador.objects.all().values('id', 'nome')

    dados = {
        'nome': coordenador.nome,
        'email': coordenador.email,
        'telefone': coordenador.telefone,
        'situacao': coordenador.situacao,
        'publicacao': coordenador.publicacao.strftime('%d/%m/%Y') if coordenador.publicacao else "Data não disponível",
        'edicao': coordenador.edicao.strftime('%d/%m/%Y') if coordenador.edicao else "Não editado",
        # 'coordenadores': list(coordenadores)
    }
    return JsonResponse(dados)

def excluir_coordenador(request, coordenador_id):
    if request.method == 'POST':
        coordenador = get_object_or_404(Coordenador, id=coordenador_id)
        coordenador.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método não permitido'})


#Curso

def criar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
def curso_lista(request):
    make_curso = CursoForm(request.POST)
    search_curso = SearchForm(request.GET)
    query = request.GET.get('query')
    cursos = Curso.objects.all()

    if query:
        cursos = cursos.filter(
            Q(nome__icontains=query) | Q(sobre__icontains=query)
        )
    
    context = {
        'make_curso': make_curso,
        'search_curso': search_curso,
        'cursos': cursos,
        'query': query,
    }

    return render(request, 'cead/pages/curso.html', context)

def detalhar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    dados = {
        'nome': curso.nome,
        'sobre': curso.sobre,
        'publicacao': curso.publicacao.strftime('%d/%m/%Y') if curso.publicacao else "Data não disponível",
        'edicao': curso.edicao.strftime('%d/%m/%Y') if curso.edicao else "Não editado",
    }
    return JsonResponse(dados)