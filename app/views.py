from django.shortcuts import render

def home(request):
    return render(request, "app/pages/home.html")

def noticias(request):
    return render(request, "app/pages/noticias.html")