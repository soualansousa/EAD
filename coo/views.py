from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import logging 

from cead.models import Noticia, NoticiaCurso, Polo, Curso, Coordenador, CursoPolo, Mediador, GestorPolos, CoordenadorCurso, Gestor, Mediacao, Disciplina, Documentos, Perguntas, Contato
from .forms import SearchForm, NoticiaForm, PoloForm, CoordenadorForm, CursoForm, MediadorForm, GestorForm, CoordenadorCursoForm, CursoPoloForm, MediacaoForm, DisciplinaForm

@login_required
def coordenacao(request):
    return render(request, "coo/pages/home.html")
    
def curso_lista_coo(request):
    coordenador_curso_id = request.session.get('coordenador_curso_id')

    if coordenador_curso_id:
        try:
            curso = Curso.objects.get(id=coordenador_curso_id)
        except Curso.DoesNotExist:
            curso = None
    else:
        curso = None
    
    context = {
        'curso': curso,
    }

    return render(request, 'coo/pages/curso.html', context)

def detalhar_cursoPolo(request, cursoPolo_id):
    curso_polos = get_object_or_404(CursoPolo, id=cursoPolo_id)
    dados = {
        'curso': curso_polos.curso.nome,
        'polo': curso_polos.polo.cidade,
        'publicacao': curso_polos.publicacao.strftime('%d/%m/%Y') if curso_polos.publicacao else "Data não disponível",
        'edicao': curso_polos.edicao.strftime('%d/%m/%Y') if curso_polos.edicao else "Não editado",
    }
    return JsonResponse(dados)

# Notícia 
def noticias_lista(request):
    coordenador_curso_id = request.session.get('coordenador_curso_id')
    make_noticia = NoticiaForm(request.POST)
    search_noticia = SearchForm(request.GET)
    query = request.GET.get('query')
    noticia_cursos = NoticiaCurso.objects.select_related('noticia', 'curso').filter(curso_id=coordenador_curso_id)

    query = request.GET.get('query', '')
    if query == 'none':
        query = ''

    if query:
        noticia_cursos = noticia_cursos.filter(
            Q(curso__nome__icontains=query) | Q(noticia__titulo__icontains=query) | Q(noticia__descricao__icontains=query)
        )

    noticia_cursos_paginada = Paginator(noticia_cursos, 10)
    p = request.GET.get("p")
    try:
        pagina = noticia_cursos_paginada.page(p)
    except PageNotAnInteger:
        pagina = noticia_cursos_paginada.page(1)
    except EmptyPage:
        pagina = noticia_cursos_paginada.page(1)

    context = {
        'make_noticia': make_noticia,
        'search_noticia': search_noticia,
        'noticia_cursos': pagina,
        'query': query,
    }

    return render(request, 'coo/pages/noticias.html', context)


def criar_noticia(request):
    coordenador_curso_id = request.session.get('coordenador_curso_id')

    if request.method == 'POST':
        form = NoticiaForm(request.POST, coordenador_curso_id=coordenador_curso_id)
        if form.is_valid():
            noticia = form.save()

            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    

def excluir_noticia(request, noticia_id):
    coordenador_curso_id = request.session.get('coordenador_curso_id')

    if not coordenador_curso_id:
        return JsonResponse({'error': 'Curso não encontrado para o coordenador.'}, status=404)

    if request.method == 'POST':
        try:
            noticia_curso = NoticiaCurso.objects.get(noticia_id=noticia_id, curso_id=coordenador_curso_id)
            noticia_curso.noticia.delete()
            noticia_curso.delete() 
            return JsonResponse({'success': True})
        except NoticiaCurso.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notícia não encontrada ou não associada ao seu curso.'})
    return JsonResponse({'success': False, 'error': 'Método não permitido'})


def detalhar_noticia(request, noticia_id):
    curso_id = request.GET.get('curso')

    try:
        noticia_curso = NoticiaCurso.objects.select_related('noticia', 'curso').get(
            noticia_id=noticia_id,
            curso_id=curso_id
        )
    except NoticiaCurso.DoesNotExist:
        return JsonResponse({'error': 'Notícia ou curso não encontrados.'}, status=404)

    dados = {
        'titulo': noticia_curso.noticia.titulo,
        'descricao': noticia_curso.noticia.descricao,
        'arquivo': noticia_curso.noticia.arquivo.url if noticia_curso.noticia.arquivo else None,
        'curso': noticia_curso.curso.nome if noticia_curso.curso else "Curso não informado",
        'publicacao': noticia_curso.noticia.publicacao.strftime('%d/%m/%Y') if noticia_curso.noticia.publicacao else "Data não disponível",
        'edicao': noticia_curso.noticia.edicao.strftime('%d/%m/%Y') if noticia_curso.noticia.edicao else "Não editado",
    }
    return JsonResponse(dados)

def editar_noticia(request, noticia_id):
    coordenador_curso_id = request.session.get('coordenador_curso_id')

    if not coordenador_curso_id:
        return JsonResponse({'error': 'Curso não encontrado para o coordenador.'}, status=404)

    noticia_curso = NoticiaCurso.objects.filter(noticia_id=noticia_id, curso_id=coordenador_curso_id).first()

    if request.method == 'POST':
        form = NoticiaForm(request.POST, instance=noticia_curso.noticia)
        if form.is_valid():
            noticia = form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    dados = {
        'titulo': noticia_curso.noticia.titulo,
        'descricao': noticia_curso.noticia.descricao,
        'arquivo': noticia_curso.noticia.arquivo.url if noticia_curso.noticia.arquivo else None,
        'publicacao': noticia_curso.noticia.publicacao.strftime('%d/%m/%Y') if noticia_curso.noticia.publicacao else "Data não disponível",
        'edicao': noticia_curso.noticia.edicao.strftime('%d/%m/%Y') if noticia_curso.noticia.edicao else "Não editado",
        'curso': noticia_curso.curso.id,
        'cursos': list(Curso.objects.all().values('id', 'nome')),
    }
    return JsonResponse(dados)
#disciplina
def criar_disciplina(request):
    # if request.method == 'POST':
    #     form = DisciplinaForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return JsonResponse({'success': True})
    #     return JsonResponse({'success': False, 'errors': form.errors})
    coordenador_curso_id = request.session.get('coordenador_curso_id')

    if request.method == 'POST':
        form = DisciplinaForm(request.POST, coordenador_curso_id=coordenador_curso_id)
        if form.is_valid():
            disciplina = form.save()

            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})

    
# def vincular_disciplina(request):
#     if request.method == 'POST':
#         form = CoordenadorCursoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'success': True})
#         return JsonResponse({'success': False, 'errors': form.errors})
    
def disciplina_lista(request):
    make_disciplina = DisciplinaForm(request.POST)
    search_disciplina = SearchForm(request.GET)
    query = request.GET.get('query')
    disciplina_cursos = Disciplina.objects.select_related('curso').all()

    query = request.GET.get('query', '')
    if query == 'none':
        query = ''

    if query:
        disciplina_cursos = disciplina_cursos.filter(
            Q(curso__nome__icontains=query) | Q(nome_icontains=query) | Q(modulo__icontains=query)
        )

    disciplina_cursos_paginada = Paginator(disciplina_cursos, 10)
    p = request.GET.get("p")
    try:
        pagina = disciplina_cursos_paginada.page(p)
    except PageNotAnInteger:
        pagina = disciplina_cursos_paginada.page(1)
    except EmptyPage:
        pagina = disciplina_cursos_paginada.page(1)

    context = {
        'make_disciplina': make_disciplina,
        'search_disciplina': search_disciplina,
        'disciplina_cursos': pagina,
        'query': query,
    }

    return render(request, 'coo/pages/disciplina.html', context)

def detalhar_disciplina(request, curso_id, coordenador_id):
    cursos = get_object_or_404(Curso, id=curso_id)
    curso_polos = CursoPolo.objects.filter(curso=cursos)
    noticia_cursos = NoticiaCurso.objects.filter(curso=cursos)
    coordenador_cursos = CoordenadorCurso.objects.filter(curso=cursos)
    mediacoes = Mediacao.objects.filter(curso_polos__curso=cursos)

    context = {
        'cursos': cursos,
        'noticia_cursos': noticia_cursos,
        'curso_polos': curso_polos,
        'coordenador_cursos': coordenador_cursos,
        'mediacoes': mediacoes,
    }

    return render(request, 'coo/pages/detalhes_curso.html', context)

def excluir_disciplina(request, cursoPolo_id):
    if request.method == 'POST':
        cursoPolo = get_object_or_404(CursoPolo, id=cursoPolo_id)
        cursoPolo.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

def detalhar_disciplina(request, cursoPolo_id):
    curso_polos = get_object_or_404(CursoPolo, id=cursoPolo_id)
    dados = {
        'curso': curso_polos.curso.nome,
        'polo': curso_polos.polo.cidade,
        'publicacao': curso_polos.publicacao.strftime('%d/%m/%Y') if curso_polos.publicacao else "Data não disponível",
        'edicao': curso_polos.edicao.strftime('%d/%m/%Y') if curso_polos.edicao else "Não editado",
    }
    return JsonResponse(dados)


