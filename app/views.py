from django.shortcuts import render
from .models import Noticia

def home(request):
    return render(request, "app/pages/home.html")

def noticias(request):
    noticias = request.GET.get(Noticia)
    return render(request, "app/pages/noticias.html", {'noticias': noticias})