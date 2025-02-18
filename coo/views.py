from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import resolve
from django.http import FileResponse
from django.conf import settings
import os
import logging 


from cead.models import Noticia, NoticiaCurso, Polo, Curso, Coordenador, CursoPolo, Mediador, GestorPolos, CoordenadorCurso, Gestor, Mediacao, Disciplina, Documentos, Perguntas

from .models import Contato

from .forms import SearchForm, NoticiaForm, PoloForm, CoordenadorForm, CursoForm, MediadorForm, GestorForm, CoordenadorCursoForm, CursoPoloForm, MediacaoForm, DisciplinaForm, ContatoForm, DocumentoForm

@login_required
def coordenacao(request):
    return render(request, "coo/pages/home.html")

#curso 
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
    cursos = Curso.objects.all()  
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
    coordenador_curso_id = request.session.get('coordenador_curso_id')
    contatos = Contato.objects.filter(curso_id=coordenador_curso_id)
    make_contato = ContatoForm(request.POST)
    search_contato = SearchForm(request.GET)
    query = request.GET.get('query')

    query = request.GET.get('query', '')
    if query == 'none':
        query = ''

    if query:
        contatos = contatos.filter(
            Q(nome__icontains=query) | Q(email__icontains=query) | Q(assunto__icontains=query)
        )

    contatos_paginada = Paginator(contatos, 10)
    p = request.GET.get("p")
    try:
        pagina = contatos_paginada.page(p)
    except PageNotAnInteger:
        pagina = contatos_paginada.page(1)
    except EmptyPage:
        pagina = contatos_paginada.page(1)

    context = {
        'make_contato': make_contato,
        'search_contato': search_contato,
        'contatos': pagina,
        'query': query,
    }

    return render(request, 'coo/pages/contato.html', context)


def editar_contato(request, contato_id):
    coordenador_curso_id = request.session.get('coordenador_curso_id')

    if not coordenador_curso_id:
        return JsonResponse({'error': 'Curso não encontrado para o coordenador.'}, status=404)

    contatos = Contato.objects.filter(contato_id=contato_id, curso_id=coordenador_curso_id).first()

    if request.method == 'POST':
        form = ContatoForm(request.POST, instance=contatos)
        if form.is_valid():
            contatos = form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    dados = {
        'nome': contatos.nome,
        'email': contatos.email,
        'telefone': contatos.telefone,
        'matricula': contatos.matricula,
        'assunto': contatos.assunto,
        'mensagem': contatos.mensagem,
        'publicacao': contatos.publicacao.strftime('%d/%m/%Y') if contatos.publicacao else "Data não disponível",
        'edicao': contatos.edicao.strftime('%d/%m/%Y') if contatos.edicao else "Não editado",
        'curso': contatos.curso.id,
        'cursos': list(Curso.objects.all().values('id', 'nome')),
    }
    return JsonResponse(dados)


def detalhar_contato(request, contato_id):
    coordenador_curso_id = request.session.get('coordenador_curso_id')
    curso_id = request.GET.get('curso')
    
    try:
        contatos = Contato.objects.filter(contato_id=contato_id, curso_id=coordenador_curso_id).get(
            curso_id=curso_id
        )
    except NoticiaCurso.DoesNotExist:
        return JsonResponse({'error': 'Contato(s) não encontrado(s).'}, status=404)

    dados = {
        'curso': contatos.curso.nome if contatos.curso else "Curso não informado",
        'nome': contatos.nome,
        'matricula': contatos.matricula,
        'email': contatos.email,
        'telefone': contatos.telefone,
        'assunto': contatos.assunto,
        'mensagem': contatos.mensagem,
        'publicacao': contatos.publicacao.strftime('%d/%m/%Y') if contatos.publicacao else "Data não disponível",
        'edicao': contatos.edicao.strftime('%d/%m/%Y') if contatos.edicao else "Não editado",
    }
    return JsonResponse(dados)



def criar_contato(request):
    coordenador_curso_id = request.session.get('coordenador_curso_id')

    if request.method == 'POST':
        form = DisciplinaForm(request.POST, coordenador_curso_id=coordenador_curso_id)
        if form.is_valid():
            contato = form.save()

            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})



def excluir_contato(request, disciplina_id):
    if request.method == 'POST':
        disciplina = get_object_or_404(Disciplina, id=disciplina_id)
        try:
            disciplina.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


#documentos publico
def documentos_publico(request):
    documentos = Documentos.objects.all().order_by('-publicacao')
    return render(request, 'coo/pages/teste_documentos.html', {'documentos': documentos})



def visualizar_documento(request, documento_id):
    documento = get_object_or_404(Documentos, id=documento_id)
    
    # Caminho completo do arquivo
    file_path = os.path.join(settings.MEDIA_ROOT, str(documento.arquivo))
    
    # Abre o arquivo e inicia o download automaticamente
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    
    return response

def visualizar_imagem(request, id):
    documento = Documentos.objects.get(id=id)
    return render(request, 'coo/pages/imagem.html', {'documento': documento})




#documentos coordenador

def documento_lista(request):
    documentos = Documentos.objects.filter()
    form = DocumentoForm()
    
    paginator = Paginator(documentos, 10)
    page_number = request.GET.get('page')
    try:
        documentos_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        documentos_paginados = paginator.page(1)
    except EmptyPage:
        documentos_paginados = paginator.page(paginator.num_pages)
    
    return render(request, 'coo/pages/documentos.html', {'documentos': documentos_paginados, 'form': form})



def criar_documento(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})


def editar_documento(request, documento_id):
    if request.method == 'POST':
        curso_id = request.GET.get('curso')
        if not curso_id:
            return JsonResponse({'success': False, 'message': 'ID do Curso não fornecido.'})

        # Obtém o documento
        documento = get_object_or_404(Documentos, id=documento_id, curso_id=curso_id)

        # Atualiza os campos
        documento.titulo = request.POST.get('titulo')
        documento.descricao = request.POST.get('descricao')
        if request.FILES.get('arquivo'):
            documento.arquivo = request.FILES['arquivo']
        documento.publicacao = request.POST.get('publicacao')
        documento.edicao = request.POST.get('edicao')

        # Salva as mudanças
        documento.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Método não permitido.'})

    

def detalhar_documento(request, documento_id):
    if request.method == "GET":
        curso_id = request.GET.get("curso")

        if not curso_id:
            return JsonResponse({"success": False, "message": "ID do Curso não fornecido."}, status=400)

        documento = get_object_or_404(Documentos, id=documento_id, curso_id=curso_id)

        dados = {
            'curso': documento.curso.nome,
            'titulo': documento.titulo,
            'descricao': documento.descricao,
            'arquivo': documento.arquivo.url if documento.arquivo else '',
            'publicacao': documento.publicacao.strftime('%d/%m/%Y'),
            'edicao': documento.edicao.strftime('%d/%m/%Y')
        }
        return JsonResponse(dados)



def excluir_documento(request, documento_id):
    if request.method == 'POST':
        curso_id = request.GET.get("curso")
        if not curso_id:
            return JsonResponse({"success": False, "message": "ID do Curso não fornecido."}, status=400)
        
        documento = get_object_or_404(Documentos, id=documento_id, curso_id=curso_id)
        try:
            documento.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    elif request.method == 'GET':
        # Caso queira tratar a requisição GET aqui, adicione um código condicional
        curso_id = request.GET.get("curso")
        if not curso_id:
            return JsonResponse({"success": False, "message": "ID do Curso não fornecido."}, status=400)
        
        documento = get_object_or_404(Documentos, id=documento_id, curso_id=curso_id)
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)


#perguntas coordenador

def perguntas_lista(request):
    query = request.GET.get('query', '')
    perguntas = Perguntas.objects.filter(pergunta__icontains=query)

  
    perguntas = perguntas.order_by('-publicacao')
    return render(request,  'coo/pages/perguntas.html', {'perguntas': perguntas, 'query': query})


def criar_pergunta(request):
    if request.method == 'POST':
        form = PerguntaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})


def editar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Perguntas, id=pergunta_id)
    if request.method == 'POST':
        form = PerguntaForm(request.POST, request.FILES, instance=pergunta)
        if form.is_valid():
            form.save()
            return redirect('perguntas_lista')
    else:
        form = PerguntaForm(instance=pergunta)
    return render(request, 'perguntas/form.html', {'form': form})


def excluir_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Perguntas, id=pergunta_id)
    pergunta.delete()
    return redirect('perguntas_lista')


def detalhar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Perguntas, id=pergunta_id)
    return render(request, 'perguntas/detalhar.html', {'pergunta': pergunta})



#pagina de testes

def pagina_teste(request):
    return render(request, 'coo/pages/teste.html')