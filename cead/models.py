from django.db import models
from datetime import date
from django.utils.safestring import mark_safe


class Curso(models.Model):
    nome = models.CharField(max_length=150)
    sobre = models.TextField()
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now=True)

    def __str__(self):
        return self.nome

class Documentos(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=150)
    descricao = models.TextField()
    arquivo = models.FileField()
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now=True)

    def __str__(self):
        return self.titulo

    def Foto(self):
        self.arquivo
        return mark_safe('<img src="{}" height="50" />' .format(self.Imagem.url))

class Disciplina(models.Model):
    MODULO_CHOICES = [
        ('1', '1º'),
        ('2', '2º'),
        ('3', '3º'),
        ]
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nome = models.CharField(max_length=150)
    ementa = models.TextField()
    modulo = models.CharField(max_length=10, choices=MODULO_CHOICES)
    ch = models.IntegerField()
    arquivo = models.FileField()
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now=True)

    def __str__(self):
        return self.nome

class Perguntas(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    pergunta = models.CharField(max_length=255)
    resposta = models.TextField()
    arquivo = models.FileField()
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now=True)

    def __str__(self):
        return self.pergunta
    
class Contato(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nome = models.CharField(max_length=150)
    email = models.EmailField(max_length=100)
    telefone = models.CharField(max_length=11)
    matricula = models.CharField(max_length=50)
    assunto = models.CharField(max_length=255)
    mensagem = models.TextField()
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now=True)

    def __str__(self):
        return self.assunto

class Coordenador(models.Model):
    SITUACAO_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
      
        ]
    nome = models.CharField(max_length=150)
    email = models.EmailField(max_length=100, default="email@exemplo.com")
    telefone = models.CharField(max_length=11, default="7499999999")
    situacao = models.CharField(max_length=10, choices=SITUACAO_CHOICES, default='ATIVO')
    publicacao = models.DateField(auto_now_add=True, null=True)
    edicao = models.DateField(auto_now=True)

    def __str__(self):
        return self.nome

class Noticia(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(max_length=900)
    arquivo = models.FileField()
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now=True)

    def __str__(self):
        return self.titulo
    
class Polo(models.Model):
    coordenador = models.ForeignKey(Coordenador, on_delete=models.CASCADE)
    cidade = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now=True)

    def __str__(self):
        return self.cidade

class Mediador(models.Model):
    SITUACAO_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
      
        ]
    nome = models.CharField(max_length=150)
    email = models.EmailField(max_length=100, default="email@exemplo.com")
    telefone = models.CharField(max_length=11, default="7499999999")
    formacao = models.TextField(max_length=255)
    situacao = models.CharField(max_length=10, choices=SITUACAO_CHOICES, default='ATIVO')
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now=True)

    def __str__(self):
        return self.nome