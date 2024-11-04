from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def coordenacao(request):
    return render(request, "coo/pages/home.html")