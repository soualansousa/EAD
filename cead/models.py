from django.db import models
from datetime import date

class Curso(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Coordenador(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Noticia(models.Model):
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
class Polo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    coordenador = models.ForeignKey(Coordenador, on_delete=models.CASCADE)
    cidade = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titulo
