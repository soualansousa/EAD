from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import logging 
from django.urls import resolve

from cead.models import Noticia, NoticiaCurso, Polo, Curso, Coordenador, CursoPolo, Mediador, GestorPolos, CoordenadorCurso, Gestor, Mediacao, Disciplina, Documentos, Perguntas

from .models import Contato

from .forms import SearchForm, NoticiaForm, PoloForm, CoordenadorForm, CursoForm, MediadorForm, GestorForm, CoordenadorCursoForm, CursoPoloForm, MediacaoForm, DisciplinaForm, ContatoForm



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

# mediador
def mediadores_lista(request):
    coordenador_curso_id = request.session.get('coordenador_curso_id')
    print(f"Coordenador Curso ID na view mediadores_lista: {coordenador_curso_id}")

    make_mediador = MediadorForm(request.POST, coordenador_curso_id=coordenador_curso_id)
    sync_mediacao = MediacaoForm(request.POST)
    search_mediador = SearchForm(request.GET)
    query = request.GET.get('query')
    mediacoes = Mediacao.objects.select_related('mediador', 'curso_polos').filter(curso_polos__curso_id=coordenador_curso_id)
   
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

    return render(request, 'coo/pages/mediadores.html', context)

def criar_mediador(request):
    coordenador_curso_id = request.session.get('coordenador_curso_id')
    print(f"Coordenador Curso ID no view: {coordenador_curso_id}")

    if request.method == 'POST':
        form = MediadorForm(request.POST, coordenador_curso_id=coordenador_curso_id)
        if form.is_valid():
            mediador = form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})


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


#disciplina
def criar_disciplina(request):
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
            Q(curso__nome__icontains=query) | Q(nome__icontains=query) | Q(modulo__icontains=query)
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



def editar_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)

    if request.method == 'GET':
        cursos = Curso.objects.all()  
        cursos_data = [{'id': curso.id, 'nome': curso.nome} for curso in cursos]
        data = {
            'curso': disciplina.curso.id,
            'nome': disciplina.nome,
            'ementa': disciplina.ementa,
            'ch': disciplina.carga_horaria,
            'cursos': cursos_data
        }
        return JsonResponse(data)

    elif request.method == 'POST':
        try:
            disciplina.curso_id = request.POST.get('curso')
            disciplina.nome = request.POST.get('nome')
            disciplina.ementa = request.POST.get('ementa')
            disciplina.carga_horaria = request.POST.get('ch')
            disciplina.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'errors': str(e)})



def excluir_disciplina(request, disciplina_id):
    if request.method == 'POST':
        disciplina = get_object_or_404(Disciplina, id=disciplina_id)
        try:
            disciplina.delete() 
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def detalhar_disciplina(request, cursoPolo_id):
    curso_polos = get_object_or_404(CursoPolo, id=cursoPolo_id)
    dados = {
        'curso': curso_polos.curso.nome,
        'polo': curso_polos.polo.cidade,
        'publicacao': curso_polos.publicacao.strftime('%d/%m/%Y') if curso_polos.publicacao else "Data não disponível",
        'edicao': curso_polos.edicao.strftime('%d/%m/%Y') if curso_polos.edicao else "Não editado",
    }
    return JsonResponse(dados)


#contatos publico

def contato_publico(request):
    cursos = Curso.objects.all()  #
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coo:contato_publico') 
    else:
        form = ContatoForm()

    return render(request, 'coo/pages/publico.html', {'form': form, 'cursos': cursos})


def enviar_contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('coo:contato_publico') 
    else:
        form = ContatoForm()

    cursos = Curso.objects.all()  
    return render(request, 'coo/pages/publico.html', {'form': form, 'cursos': cursos})

#contato coordenador

def contato_lista(request):
    from django.shortcuts import render, redirect
from .models import Contato
from cead.models import Curso

def contato_lista(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        assunto = request.POST.get('assunto')
        mensagem = request.POST.get('mensagem')
        curso_id = request.POST.get('curso')

        if curso_id:
            curso = Curso.objects.get(id=curso_id)
            contato = Contato(curso=curso, nome=nome, email=email, telefone=telefone, assunto=assunto, mensagem=mensagem)
            contato.save()

            # Redirecionar ou exibir mensagem de sucesso
            return redirect('coo:contato_lista')  # ou você pode redirecionar para uma página de sucesso
        else:
            # Se não houver curso selecionado, você pode exibir um erro ou mensagem de alerta
            return render(request, 'contato_form.html', {'erro': 'Curso é obrigatório'})

    # Se a requisição for GET, exiba os dados salvos
    contatos = Contato.objects.all()  # Ou filtrar conforme necessário
    return render(request, 'coo/pages/contato.html', {'contatos': contatos})


    # Criar a instância do Paginator com 10 contatos por página
    paginator = Paginator(contatos, 10)

    # Pega o número da página da URL
    page_number = request.GET.get('page')

    try:
        # Tenta obter a página solicitada
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Se o número da página não for inteiro, mostra a página 1
        page_obj = paginator.page(1)
    except EmptyPage:
        # Se a página solicitada estiver fora do intervalo, mostra a última página
        page_obj = paginator.page(paginator.num_pages)

    # Contexto com a página de contatos e outras informações
    context = {
        'contatos': page_obj,
    }

    return render(request, 'coo/pages/contato.html', context)


def editar_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    cursos = Curso.objects.all()

    if request.method == 'GET':
        # Retorna os dados do contato para preencher o modal
        return JsonResponse({
            'curso': contato.curso.nome,
            'nome': contato.nome,
            'email': contato.email,
            'telefone': contato.telefone,
            'assunto': contato.assunto,
            'mensagem': contato.mensagem,
        })

    if request.method == 'POST':
        form = ContatoForm(request.POST, instance=contato)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


def detalhar_contato(request, contato_id):
    if request.method == "GET":
        curso_polos_id = request.GET.get("curso")
        if not curso_polos_id:
            return JsonResponse({"success": False, "message": "ID do CursoPolo não fornecido."})

        contato = get_object_or_404(Contato, contato_id=contato_id, curso_polos_id=curso_polos_id)
    dados = {
        'curso_polo': f"{contato.curso_polos.curso.nome} - {contato.curso_polos.polo.cidade}",
        'nome': contato.nome,
        'email': contato.email,
        'assunto': contato.assunto,
        'publicacao': contato.publicacao.strftime('%d/%m/%Y') if contato.publicacao else "Data não disponível",
        'edicao': contato.edicao.strftime('%d/%m/%Y') if contato.edicao else "Não editado",
    }
    return JsonResponse(dados)





def criar_contato(request):
    coordenador_curso_id = request.session.get('coordenador_curso_id')

    if request.method == 'POST':
        form = DisciplinaForm(request.POST, coordenador_curso_id=coordenador_curso_id)
        if form.is_valid():
            disciplina = form.save()

            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})



def excluir_contato(request, disciplina_id):
    if request.method == 'POST':
        disciplina = get_object_or_404(Disciplina, id=disciplina_id)
        try:
            disciplina.delete()  # Exclui a disciplina
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})








def pagina_teste(request):
    return render(request, 'coo/pages/teste.html')