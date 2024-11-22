from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q



from .models import Noticia, Polo, Curso, Coordenador, CursoPolo, Mediador, GestorPolos, CoordenadorCurso, Gestor
from .forms import SearchForm, NoticiaForm, PoloForm, CoordenadorForm, CursoForm, MediadorForm, GestorForm



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
        'arquivo': noticia.arquivo.url if noticia.arquivo else None,
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
        'arquivo': noticia.arquivo.url if noticia.arquivo else None,
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

    query = request.GET.get('query', '')
    if query == 'none':
        query = ''  # Corrige o valor se for "none"

    if query:
        noticias = noticias.filter(
            Q(titulo__icontains=query) | Q(descricao__icontains=query) | Q(edicao__icontains=query) | Q(publicacao__icontains=query)| Q(arquivo__icontains=query)
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
    polos = Polo.objects.all().order_by('cidade')

    query = request.GET.get('query', '').strip()
    if query.lower() == 'none':
        query = '' 

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
    coordenador_cursos = CoordenadorCurso.objects.select_related('coordenador', 'curso').all()

    query = request.GET.get('query', '')
    if query == 'none':
        query = ''  # Corrige o valor se for "none"

    if query:
        coordenador_cursos = coordenador_cursos.filter(
        Q(coordenador__situacao__icontains=query) |
        Q(coordenador__edicao__icontains=query) |
        Q(coordenador__publicacao__icontains=query) |
        Q(coordenador__nome__icontains=query) |
        Q(coordenador__telefone__icontains=query) |
        Q(coordenador__email__icontains=query)
        )

    context = {
        'make_coordenador': make_coordenador,
        'search_coordenador': search_coordenador,
        'coordenador_cursos': coordenador_cursos,
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
    
    coordenador_curso = CoordenadorCurso.objects.filter(coordenador_id=coordenador_id).first()


    if request.method == 'POST': 
        form = CoordenadorForm(request.POST, instance=coordenador)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})

    cursos = Curso.objects.all().values('id', 'nome')

    curso_relacionado = coordenador_curso.curso.id if coordenador_curso else None


    dados = {
        'nome': coordenador.nome,
        'email': coordenador.email,
        'telefone': coordenador.telefone,
        'situacao': coordenador.situacao,
        'publicacao': coordenador.publicacao.strftime('%d/%m/%Y') if coordenador.publicacao else "Data não disponível",
        'edicao': coordenador.edicao.strftime('%d/%m/%Y') if coordenador.edicao else "Não editado",
        'curso': curso_relacionado,
        'cursos': list(cursos),
        
    }
    return JsonResponse(dados)

def excluir_coordenador(request, coordenador_id):
    if request.method == 'POST':
        coordenador = get_object_or_404(Coordenador, id=coordenador_id)
        coordenador.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método não permitido'})


# mediador

def mediadores_lista(request):
    make_mediador = MediadorForm(request.POST)
    search_mediador = SearchForm(request.GET)
    query = request.GET.get('query')
    mediadores = Mediador.objects.all()

    query = request.GET.get('query', '')
    if query == 'none':
        query = ''  # Corrige o valor se for "none"


    if query:
        mediadores = mediadores.filter(
        Q(situacao__icontains=query) |
        Q(edicao__icontains=query) |
        Q(publicacao__icontains=query) |
        Q(nome__icontains=query) |
        Q(telefone__icontains=query) |
        Q(email__icontains=query)
        )
    
    context = {
        'make_mediador': make_mediador,
        'search_mediador': search_mediador,
        'mediadores': mediadores,
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


def detalhar_mediador(request, mediador_id):
    mediador = get_object_or_404(Mediador, id=mediador_id)
    dados = {
        'cursoPolo': mediador.curso_polo,
        'nome': mediador.nome,
        'email': mediador.email,
        'telefone': mediador.telefone,
        'formacao': mediador.formacao,
        'situacao': "Ativo" if mediador.situacao else "Inativo",
        'publicacao': mediador.publicacao.strftime('%d/%m/%Y') if mediador.publicacao else "Data não disponível",
        'edicao': mediador.edicao.strftime('%d/%m/%Y') if mediador.edicao else "Não editado",
    }
    return JsonResponse(dados)
 

def editar_mediador(request, mediador_id):
    mediador = get_object_or_404(Mediador, id=mediador_id)
    
    if request.method == 'POST':
       
        mediador.situacao = request.POST.get('situacao')
        mediador.curso_polo = request.POST.get('nome')
        mediador.nome = request.POST.get('nome')
        mediador.email = request.POST.get('email')
        mediador.telefone = request.POST.get('telefone')
        mediador.formacao = request.POST.get('formacao')

        mediador.save()


            
        return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
   

    dados = {
        'nome': mediador.nome,
        'email': mediador.email,
        'telefone': mediador.telefone,
        'formacao': mediador.formacao,
        'situacao': mediador.situacao,
        'publicacao': mediador.publicacao.strftime('%d/%m/%Y') if mediador.publicacao else "Data não disponível",
        'edicao': mediador.edicao.strftime('%d/%m/%Y') if mediador.edicao else "Não editado",
        
    }
    return JsonResponse(dados)

def excluir_mediador(request, coordenador_id):
    if request.method == 'POST':
        mediador = get_object_or_404(Mediador, id=mediador_id)
        mediador.delete()
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
    cursos = get_object_or_404(Curso, id=curso_id)
    polos = get_object_or_404(Polo, id=curso_id)
    noticias = Noticia.objects.filter(curso=cursos)
    curso_polos = CursoPolo.objects.filter(curso=cursos)
    coordenadores = Coordenador.objects.filter(curso=cursos)

    return render(request, 'cead/pages/detalhes_curso.html', {
        'cursos': cursos,
        'polos': polos,
        'noticias': noticias,
        'curso_polos': curso_polos,
        'coordenadores': coordenadores,
    })

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
    make_gestor = GestorForm(request.POST)
    search_gestor = SearchForm(request.GET)
    query = request.GET.get('query')
    gestores = Gestor.objects.all().order_by('situacao', 'nome')


    query = request.GET.get('query', '')
    if query == 'none':
        query = ''  


    if query:
        gestores = gestores.filter(
        Q(situacao__icontains=query) |
        Q(edicao__icontains=query) |
        Q(publicacao__icontains=query) |
        Q(nome__icontains=query) |
        Q(telefone__icontains=query) |
        Q(email__icontains=query)
        )
    
    context = {
        'make_gestor': make_gestor,
        'search_gestor': search_gestor,
        'gestores': gestores,
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
    else:
        form = GestorFormorForm()
    return render(request, 'modais_gestores.html', {'form': form})


def detalhar_gestor(request, gestor_id):
    gestor = get_object_or_404(Gestor, id=gestor_id)
    dados = {
        
        'nome': gestor.nome,
        'email': gestor.email,
        'telefone': gestor.telefone,
        'formacao': gestor.formacao,
        'situacao': "Ativo" if gestor.situacao else "Inativo",
        'publicacao': gestor.publicacao.strftime('%d/%m/%Y') if gestor.publicacao else "Data não disponível",
        'edicao': gestor.edicao.strftime('%d/%m/%Y') if gestor.edicao else "Não editado",
    }
    return JsonResponse(dados)
 

def editar_gestor(request, gestor_id):
    gestor = get_object_or_404(Gestor, id=gestor_id)
    
    if request.method == 'POST':
       
        gestor.situacao = request.POST.get('situacao')
        gestor.nome = request.POST.get('nome')
        gestor.email = request.POST.get('email')
        gestor.telefone = request.POST.get('telefone')
        gestor.formacao = request.POST.get('formacao')

        gestor.save()


            
        return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
   

    dados = {
        'nome': gestor.nome,
        'email': gestor.email,
        'telefone': gestor.telefone,
        'formacao': gestor.formacao,
        'situacao': gestor.situacao,
        'publicacao': gestor.publicacao.strftime('%d/%m/%Y') if gestor.publicacao else "Data não disponível",
        'edicao': gestor.edicao.strftime('%d/%m/%Y') if gestor.edicao else "Não editado",
        
    }
    return JsonResponse(dados)

def excluir_gestor(request, gestor_id):
    if request.method == 'POST':
        gestor = get_object_or_404(Gestor, id=gestor_id)
        gestor.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método não permitido'})
