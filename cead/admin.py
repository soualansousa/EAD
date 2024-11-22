from django.contrib import admin
from .models import Noticia, Curso, Polo, Coordenador, Documentos, Disciplina, Perguntas, Contato, Mediador, CursoPolo, Cead, CoordenadorCurso

admin.site.register(Noticia),
admin.site.register(Cead),
admin.site.register(Curso),
admin.site.register(Coordenador),
admin.site.register(Polo),
admin.site.register(Documentos),
admin.site.register(Disciplina),
admin.site.register(Perguntas),
admin.site.register(Contato),
admin.site.register(Mediador),
admin.site.register(CursoPolo),
admin.site.register(CoordenadorCurso),