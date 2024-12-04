from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import logging 

from .models import Noticia, NoticiaCurso, Polo, Curso, Coordenador, CursoPolo, Mediador, GestorPolos, CoordenadorCurso, Gestor, Mediacao
from .forms import SearchForm, NoticiaForm, PoloForm, CoordenadorForm, CursoForm, MediadorForm, GestorForm, CoordenadorCursoForm, CursoPoloForm, MediacaoForm

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

def noticias_lista(request):
    make_noticia = NoticiaForm(request.POST)
    search_noticia = SearchForm(request.GET)
    query = request.GET.get('query')
    noticia_cursos = NoticiaCurso.objects.select_related('noticia', 'curso').all()

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

    return render(request, 'cead/pages/noticias.html', context)

def excluir_noticia(request, noticia_id):
    if request.method == 'POST':
        noticia = get_object_or_404(Noticia, id=noticia_id)
        noticia.delete()
        return JsonResponse({'success': True})
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
    curso_id = request.GET.get('curso')
    noticia_curso = NoticiaCurso.objects.filter(noticia_id=noticia_id, curso_id=curso_id).first()

    if request.method == 'POST':
        form = NoticiaForm(request.POST, instance=noticia_curso.noticia, noticia_curso=noticia_curso)
        if form.is_valid():
            noticia = form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    cursos = Curso.objects.all().values('id', 'nome')
    curso_relacionado = noticia_curso.curso.id if noticia_curso else None
    dados = {
        'titulo': noticia_curso.noticia.titulo,
        'descricao': noticia_curso.noticia.descricao,
        'arquivo': noticia_curso.noticia.arquivo.url if noticia_curso.noticia.arquivo else None,
        'publicacao': noticia_curso.noticia.publicacao.strftime('%d/%m/%Y') if noticia_curso.noticia.publicacao else "Data não disponível",
        'edicao': noticia_curso.noticia.edicao.strftime('%d/%m/%Y') if noticia_curso.noticia.edicao else "Não editado",
        'curso': curso_relacionado,
        'cursos': list(cursos)
    }
    return JsonResponse(dados)

# polo
def polos_lista(request):
    make_polo = PoloForm(request.POST)
    sync_curso_polo = CursoPoloForm(request.POST)
    search_polo = SearchForm(request.GET)
    query = request.GET.get('query', '').strip()

    gestor_polos = GestorPolos.objects.select_related('polo', 'gestor').order_by('polo__cidade')
    
    if query.lower() == 'none':
        query = '' 

    if query:
        gestor_polos = gestor_polos.filter(
            Q(polo__cidade__icontains=query) | Q(gestor__nome__icontains=query)
        )

    gestor_polos_paginada = Paginator(gestor_polos, 10)
    p = request.GET.get("p")
    try:
        pagina = gestor_polos_paginada.page(p)
    except PageNotAnInteger:
        pagina = gestor_polos_paginada.page(1)
    except EmptyPage:
        pagina = gestor_polos_paginada.page(1)

    context = {
        'make_polo': make_polo,
        'sync_curso_polo': sync_curso_polo,
        'search_polo': search_polo,
        'gestor_polos': pagina,
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
    
def vincular_curso_polo(request):
    if request.method == 'POST':
        form = CursoPoloForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CursoPoloForm()
        return render(request, 'modais_polo.html', {'form': form})

def excluir_polo(request, polo_id):
    if request.method == 'POST':
        gestor_id = request.POST.get("gestor")  
        if not gestor_id:
            return JsonResponse({"success": False, "message": "ID do Gestor não fornecido."})
        gestor_polos = get_object_or_404(GestorPolos, polo_id=polo_id, gestor_id=gestor_id)
        gestor_polos.delete() 
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método não permitido'})


def detalhar_polo(request, polo_id):
    gestor_id = request.GET.get('gestor')

    try:
        gestor_polos = GestorPolos.objects.select_related('polo', 'gestor').get(
            gestor_id=gestor_id,
            polo_id=polo_id
        )
    except GestorPolos.DoesNotExist:
        return JsonResponse({'error': 'Polo ou gestor não encontrados.'}, status=404)

    dados = {
        'cidade': gestor_polos.polo.cidade,
        'latitude': gestor_polos.polo.latitude,
        'longitude': gestor_polos.polo.longitude,
        'gestor': gestor_polos.gestor.nome if gestor_polos.gestor.nome else "Coordenador não informado",
        'situacao': gestor_polos.situacao,
        'publicacao':gestor_polos.polo.publicacao.strftime('%d/%m/%Y') if gestor_polos.polo.publicacao else "Data não disponível",
        'edicao': gestor_polos.polo.publicacao.strftime('%d/%m/%Y') if gestor_polos.polo.publicacao else "Não editado",
        'saida': gestor_polos.saida.strftime('%d/%m/%Y') if gestor_polos.saida else "Data não disponível",
    }
    return JsonResponse(dados)


def editar_polo(request, polo_id):
    gestor_id = request.GET.get("gestor")
    gestor_polos = GestorPolos.objects.filter(polo_id=polo_id, gestor_id=gestor_id).first()

    if request.method == 'POST':
        form = PoloForm(request.POST, instance=gestor_polos.polo, gestor_polos=gestor_polos)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    
    gestores = Gestor.objects.all().values('id', 'nome')
    gestor_relacionado = gestor_polos.gestor.id if gestor_polos else None

    dados = {
        'cidade': gestor_polos.polo.cidade,
        'latitude': gestor_polos.polo.latitude,
        'longitude': gestor_polos.polo.longitude,
        'gestor': gestor_relacionado,
        'gestores': list(gestores)
    }
    return JsonResponse(dados)

# coordenador
def coordenadores_lista(request):
    make_coordenador = CoordenadorForm(request.POST)
    sync_coordenador = CoordenadorCursoForm(request.POST)
    search_coordenador = SearchForm(request.GET)
    query = request.GET.get('query')
    coordenador_cursos = CoordenadorCurso.objects.select_related('coordenador', 'curso').all()

    query = request.GET.get('query', '')
    if query == 'none':
        query = ''

    if query:
        coordenador_cursos = coordenador_cursos.filter(
        Q(coordenador__nome__icontains=query) | Q(curso__nome__icontains=query) | Q(coordenador__email__icontains=query)
        )

    coordenador_cursos_paginada = Paginator(coordenador_cursos, 10)
    p = request.GET.get("p")
    try:
        pagina = coordenador_cursos_paginada.page(p)
    except PageNotAnInteger:
        pagina = coordenador_cursos_paginada.page(1)
    except EmptyPage:
        pagina = coordenador_cursos_paginada.page(1)

    context = {
        'make_coordenador': make_coordenador,
        'sync_coordenador': sync_coordenador,
        'search_coordenador': search_coordenador,
        'coordenador_cursos': pagina,
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

def vincular_curso_coordenador(request):
    if request.method == 'POST':
        form = CoordenadorCursoForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CoordenadorCursoForm()
    return render(request, 'modais_coordenadores.html', {'form': form})

def detalhar_coordenador(request, coordenador_id):
    curso_id = request.GET.get('curso')
    
    try:
        coordenador_cursos = CoordenadorCurso.objects.select_related('coordenador', 'curso').get(
            coordenador_id=coordenador_id,
            curso_id=curso_id
        )
    except CoordenadorCurso.DoesNotExist:
        return JsonResponse({'error': 'Coordenador ou curso não encontrados.'}, status=404)

    dados = {
        'curso': coordenador_cursos.curso.nome,
        'nome': coordenador_cursos.coordenador.nome,
        'email': coordenador_cursos.coordenador.email,
        'telefone': coordenador_cursos.coordenador.telefone,
        'situacao': coordenador_cursos.situacao,
        'publicacao': coordenador_cursos.coordenador.publicacao.strftime('%d/%m/%Y') if coordenador_cursos.coordenador.publicacao else "Data não disponível",
        'edicao': coordenador_cursos.coordenador.edicao.strftime('%d/%m/%Y') if coordenador_cursos.coordenador.edicao else "Não editado",
        'saida': coordenador_cursos.saida.strftime('%d/%m/%Y') if coordenador_cursos.saida else "Data não disponível",
    }
    return JsonResponse(dados)

def editar_coordenador(request, coordenador_id):
    curso_id = request.GET.get('curso')
    coordenador_curso = CoordenadorCurso.objects.filter(coordenador_id=coordenador_id, curso_id=curso_id).first()

    if request.method == 'POST':
        form = CoordenadorForm(request.POST, instance=coordenador_curso.coordenador, coordenador_curso=coordenador_curso)
        if form.is_valid():
            coordenador_form = form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})

    cursos = Curso.objects.all().values('id', 'nome')
    curso_relacionado = coordenador_curso.curso.id if coordenador_curso else None

    dados = {
        'nome': coordenador_curso.coordenador.nome,
        'email': coordenador_curso.coordenador.email,
        'telefone': coordenador_curso.coordenador.telefone,
        'saida': coordenador_curso.saida.strftime('%Y-%m-%d') if coordenador_curso and coordenador_curso.saida else "",
        'curso': curso_relacionado,
        'cursos': list(cursos),
    }
    return JsonResponse(dados)

def excluir_coordenador(request, coordenador_id):
    if request.method == 'POST':
        curso_id = request.GET.get("curso")
        if not curso_id:
            return JsonResponse({"success": False, "message": "ID do Curso não fornecido."})
         
        coordenador_cursos = get_object_or_404(CoordenadorCurso, coordenador_id=coordenador_id, curso_id=curso_id)
        coordenador_cursos.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

# mediador
def mediadores_lista(request):
    make_mediador = MediadorForm(request.POST)
    sync_mediacao = MediacaoForm(request.POST)
    search_mediador = SearchForm(request.GET)
    query = request.GET.get('query')
    mediacoes = Mediacao.objects.select_related('mediador', 'curso_polos').all()

    query = request.GET.get('query', '')
    if query == 'none':
        query = ''

    if query:
        mediacoes = mediacoes.filter(
        Q(mediador__nome__icontains=query)
        )
    
    mediacoes_paginada = Paginator(mediacoes, 10)
    p = request.GET.get("p")
    try:
        pagina = mediacoes_paginada.page(p)
    except PageNotAnInteger:
        pagina = mediacoes_paginada.page(1)
    except EmptyPage:
        pagina = mediacoes_paginada.page(1)

    context = {
        'make_mediador': make_mediador,
        'sync_mediacao': sync_mediacao,
        'search_mediador': search_mediador,
        'mediacoes': pagina,
        'query': query,
    }

    return render(request, 'cead/pages/mediadores.html', context)

def criar_mediador(request):
    if request.method == 'POST':
        form = MediadorForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = MediadorForm()
    return render(request, 'modais_mediadores.html', {'form': form})

def mediacao(request):
    if request.method == 'POST':
        form = MediacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = MediacaoForm()
    return render(request, 'modais_mediadores.html', {'form': form})

def detalhar_mediador(request, mediador_id):
    if request.method == "GET":
        curso_polos_id = request.GET.get("curso")
        if not curso_polos_id:
            return JsonResponse({"success": False, "message": "ID do CursoPolo não fornecido."})

        mediacao = get_object_or_404(Mediacao, mediador_id=mediador_id, curso_polos_id=curso_polos_id)
        
    dados = {
        'curso_polo': f"{mediacao.curso_polos.curso.nome} - {mediacao.curso_polos.polo.cidade}",
        'nome': mediacao.mediador.nome,
        'email': mediacao.mediador.email,
        'telefone': mediacao.mediador.telefone,
        'formacao': mediacao.mediador.formacao,
        'modalidade': mediacao.modalidade,
        'situacao': mediacao.situacao,
        'publicacao': mediacao.mediador.publicacao.strftime('%d/%m/%Y') if mediacao.mediador.publicacao else "Data não disponível",
        'edicao': mediacao.mediador.edicao.strftime('%d/%m/%Y') if mediacao.mediador.edicao else "Não editado",
        'saida': mediacao.saida.strftime('%d/%m/%Y') if mediacao.saida else "Data não disponível",
    }
    return JsonResponse(dados)

def editar_mediador(request, mediador_id):
    curso_polos_id = request.GET.get("curso")
    mediacao = Mediacao.objects.filter(mediador_id=mediador_id, curso_polos_id=curso_polos_id).first()
    
    if not mediacao:
        return JsonResponse({'success': False, 'message': 'Mediacao não encontrada.'}, status=404)

    if request.method == 'POST':
        form = MediadorForm(request.POST, instance=mediacao.mediador, mediacao=mediacao, curso_polos_id=curso_polos_id)
        if form.is_valid():
            mediacao_form = form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})

    curso_polos = CursoPolo.objects.all()

    dados = {
        'nome': mediacao.mediador.nome,
        'email': mediacao.mediador.email,
        'telefone': mediacao.mediador.telefone,
        'formacao': mediacao.mediador.formacao,
        'modalidade': mediacao.modalidade,
        'saida': mediacao.saida.strftime('%Y-%m-%d') if mediacao and mediacao.saida else "",
        'curso_polos': [
            {'id': cp.id, 'nome': f"{cp.curso.nome} - {cp.polo.cidade}"}
            for cp in curso_polos
        ],
        'curso_polos_selecionado': curso_polos_id,
    }
    return JsonResponse(dados)

def excluir_mediador(request, mediador_id):
    if request.method == 'POST':
        curso_polos_id = request.GET.get("curso")
        if not curso_polos_id:
            return JsonResponse({"success": False, "message": "ID do CursoPolo não fornecido."})
        
        mediacao = get_object_or_404(Mediacao, mediador_id=mediador_id, curso_polos_id=curso_polos_id)
        mediacao.delete()
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
    
def vincular_curso(request):
    if request.method == 'POST':
        form = CoordenadorCursoForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
def curso_lista(request):
    make_curso = CursoForm(request.POST)
    sync_curso = CoordenadorCursoForm(request.POST)
    search_curso = SearchForm(request.GET)
    query = request.GET.get('query')
    coordenador_cursos = CoordenadorCurso.objects.all()
    cursos_vinculados_ids = coordenador_cursos.values_list('curso_id', flat=True)
    cursos_nao_vinculados = Curso.objects.exclude(id__in=cursos_vinculados_ids)

    if query:
        coordenador_cursos = coordenador_cursos.filter(
            Q(coordenador_cursos__nome__icontains=query) | Q(coordenador_cursos_sobre__icontains=query)
        )
    
    context = {
        'make_curso': make_curso,
        'sync_curso': sync_curso,
        'search_curso': search_curso,
        'coordenador_cursos': coordenador_cursos,
        'cursos_nao_vinculados': cursos_nao_vinculados,
        'query': query,
    }

    return render(request, 'cead/pages/curso.html', context)

def detalhar_curso(request, curso_id):
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

    return render(request, 'cead/pages/detalhes_curso.html', context)

def excluir_cursoPolo(request, cursoPolo_id):
    if request.method == 'POST':
        cursoPolo = get_object_or_404(CursoPolo, id=cursoPolo_id)
        cursoPolo.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

def detalhar_cursoPolo(request, cursoPolo_id):
    curso_polos = get_object_or_404(CursoPolo, id=cursoPolo_id)
    dados = {
        'curso': curso_polos.curso.nome,
        'polo': curso_polos.polo.cidade,
        'publicacao': curso_polos.publicacao.strftime('%d/%m/%Y') if curso_polos.publicacao else "Data não disponível",
        'edicao': curso_polos.edicao.strftime('%d/%m/%Y') if curso_polos.edicao else "Não editado",
    }
    return JsonResponse(dados)

#gestor 
def gestores_lista(request):
    make_gestor = GestorForm(request.GET)
    search_gestor = SearchForm(request.GET)
    query = request.GET.get('query', '')
    
    gestores = Gestor.objects.all()
    if query:
        gestores = gestores.filter(
            Q(situacao__icontains=query) |
            Q(nome__icontains=query) |
            Q(telefone__icontains=query) |
            Q(email__icontains=query)
        )

    gestores_paginada = Paginator(gestores, 10)
    p = request.GET.get("p")
    try:
        pagina = gestores_paginada.page(p)
    except PageNotAnInteger:
        pagina = gestores_paginada.page(1)
    except EmptyPage:
        pagina = gestores_paginada.page(1)

    context = {
        'make_gestor': make_gestor,
        'search_gestor': search_gestor,
        'gestores': pagina,
        'query': query,
    }

    return render(request, 'cead/pages/gestores.html', context)
    
def criar_gestor(request):
    if request.method == 'POST':
        form = GestorForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Método inválido'})

def detalhar_gestor(request, gestor_id):
    gestores = get_object_or_404(Gestor, id=gestor_id)
    dados = {
        'nome': gestores.nome,
        'email': gestores.email,
        'telefone': gestores.telefone,
        'formacao': gestores.formacao,
        'publicacao': gestores.publicacao.strftime('%d/%m/%Y') if gestores.publicacao else "Data não disponível",
        'edicao': gestores.edicao.strftime('%d/%m/%Y') if gestores.edicao else "Não editado",
    }
    return JsonResponse(dados)

def editar_gestor(request, gestor_id):
    gestores = Gestor.objects.filter(id=gestor_id).first()

    if request.method == 'POST':
        form = GestorForm(request.POST, instance=gestores)
        if form.is_valid():
            gestor = form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})

    dados = {
        'nome': gestores.nome,
        'email': gestores.email,
        'telefone': gestores.telefone,
        'formacao': gestores.formacao,
        'publicacao': gestores.publicacao.strftime('%d/%m/%Y') if gestores.publicacao else "Data não disponível",
        'edicao': gestores.edicao.strftime('%d/%m/%Y') if gestores.edicao else "Não editado",
    }
    return JsonResponse(dados)

def excluir_gestor(request, gestor_id):
    if request.method == 'POST':
        gestor = get_object_or_404(Gestor, id=gestor_id)
        gestor.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método não permitido'})