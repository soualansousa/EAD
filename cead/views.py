from django.shortcuts import render, redirect, get_object_or_404
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
                return redirect("cead:home_cead")
            return redirect("cead:home_coo")
    else:
        form = AuthenticationForm()
    return render(request, 'cead/pages/login.html', {'form': form})

@login_required
def home_cead(request):
    return render(request, "cead/pages/home_cead.html")

@login_required
def home_coo(request):
    return render(request, "cead/pages/home_coo.html")

def noticias_lista(request):
    noticias = Noticia.objects.all()  # Obtém todas as notícias
    return render(request, 'cead/pages/noticias.html', {'noticias': noticias})

def visualizar_noticia(request, id):
    noticia = get_object_or_404(Noticia, id=id)
    return render(request, 'cead/partials/visualizar_noticia.html', {'noticia': noticia})

def editar_noticia(request, id):
    noticia = get_object_or_404(Noticia, id=id)
    if request.method == 'POST':
        noticia.titulo = request.POST['titulo']
        noticia.descricao = request.POST['descricao']
        noticia.edicao = request.POST['edicao']
        noticia.save()
        return redirect('lista_noticias')
    return render(request, 'noticias/editar_noticia.html', {'noticia': noticia})

def remover_noticia(request, id):
    noticia = get_object_or_404(Noticia, id=id)
    if request.method == 'POST':
        noticia.delete()
        return redirect('lista_noticias')
    return render(request, 'noticias/remover_noticia.html', {'noticia': noticia})