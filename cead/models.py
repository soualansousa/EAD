from django.db import models
from datetime import date
from django.utils.safestring import mark_safe

class Cead(models.Model):
    SITUACAO_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
      
        ]
    nome = models.CharField(max_length=150)
    email = models.EmailField(max_length=100, default="email@exemplo.com")
    telefone = models.IntegerField(default="7499999999")
    situacao = models.CharField(max_length=10, choices=SITUACAO_CHOICES, default='ATIVO')
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now=True)

    def __str__(self):
        return self.nome

class Coordenador(models.Model):
    SITUACAO_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
      
        ]
    nome = models.CharField(max_length=150)
    email = models.EmailField(max_length=100, default="email@exemplo.com")
    telefone = models.IntegerField(default="7499999999")
    situacao = models.CharField(max_length=10, choices=SITUACAO_CHOICES, default='ATIVO')
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now=True)

    def __str__(self):
        return self.nome

class Curso(models.Model):
    coordenador = models.ForeignKey(Coordenador, on_delete=models.CASCADE)
    nome = models.CharField(max_length=150)
    sobre = models.TextField()
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now=True)

    def __str__(self):
        return self.nome
    
class CoordenadorCurso(models.Model):
    coordenador = models.ForeignKey(Coordenador, on_delete=models.CASCADE, related_name="coordenador_curso")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="coordenador_curso")
    entrada = models.DateField(auto_now_add=True)
    saida = models.DateField(blank=True, null=True)
    
    @property
    def situacao(self):
        return 'Ativo' if not self.saida else 'Inativo'

    def __str__(self):
        return f"{self.coordenador.nome} - {self.curso.nome}"

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

class Noticia(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(max_length=900)
    arquivo = models.FileField(blank=True)
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now=True)

    def __str__(self):
        return self.titulo

class NoticiaCurso(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name="noticia_curso")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="noticia_curso")
    
    def __str__(self):
        return f"{self.noticia.titulo} - {self.curso.nome}"

class Gestor(models.Model):
    SITUACAO_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
      
        ]
    nome = models.CharField(max_length=150)
    email = models.EmailField(max_length=100, default="email@exemplo.com")
    telefone = models.IntegerField(default="7499999999")
    situacao = models.CharField(max_length=10, choices=SITUACAO_CHOICES, default='ATIVO')
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now=True)
    formacao = models.TextField(max_length=255)

    def __str__(self):
        return self.nome

class Polo(models.Model):
    cidade = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now=True)

    def __str__(self):
        return self.cidade

class CursoPolo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="curso_polos")
    polo = models.ForeignKey(Polo, on_delete=models.CASCADE, related_name="curso_polos")
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"{self.curso.nome} - {self.polo.cidade}"

class Mediador(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(max_length=100, default="email@exemplo.com")
    telefone = models.CharField(max_length=11, default="7499999999")
    formacao = models.TextField(max_length=255)
    publicacao = models.DateField(auto_now_add=True)
    edicao = models.DateField(auto_now=True)

    def __str__(self):
        return self.nome

class Mediacao(models.Model):
    MODALIDADE_CHOICES = [
        ('PRESENCIAL', 'Presencial'),
        ('VIRTUAL', 'Virtual'),
      
        ]
    mediador = models.ForeignKey(Mediador, on_delete=models.CASCADE, related_name="Mediacao")
    curso_polos = models.ForeignKey(CursoPolo, on_delete=models.CASCADE, related_name="Mediacao")
    modalidade = models.CharField(max_length=10, choices=MODALIDADE_CHOICES, default="VIRTUAL")
    entrada = models.DateField(auto_now_add=True)
    saida = models.DateField(blank=True, null=True)
    
    @property
    def situacao(self):
        return 'Ativo' if not self.saida else 'Inativo'

    def __str__(self):
        return f"{self.mediador.nome} - {self.curso_polos}"

class GestorPolos(models.Model):
    gestor = models.ForeignKey(Gestor, on_delete=models.CASCADE, related_name="gestor_polos")
    polo = models.ForeignKey(Polo, on_delete=models.CASCADE, related_name="gestor_polos")
    entrada = models.DateField(auto_now_add=True)
    saida = models.DateField(blank=True, null=True)
    
    @property
    def situacao(self):
        return 'Ativo' if not self.saida else 'Inativo'

    def __str__(self):
        return f"{self.gestor.nome} - {self.polo.cidade}"