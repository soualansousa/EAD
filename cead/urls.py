from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name= 'cead'

urlpatterns = [
    path('',views.cead, name="cead"),

#gestores
    path('gestores/', views.gestores_lista, name="gestor_lista"), 
    path('criar_gestor/', views.criar_gestor, name='criar_gestor'),
    path('excluir_gestor/<int:gestor_id>/', views.excluir_gestor, name='excluir_gestor'),
    path('detalhar_gestor/<int:gestor_id>/', views.detalhar_gestor, name='detalhar_gestor'),
    path('editar_gestor/<int:gestor_id>/', views.editar_gestor, name='editar_gestor'),

#notícias
    path('noticias/',views.noticias_lista, name="noticia_lista"),
    path('criar_noticia/', views.criar_noticia, name='criar_noticia'),
    path('noticias/excluir_noticia/<int:noticia_id>/', views.excluir_noticia, name='excluir_noticia'),
    path('noticias/detalhar_noticia/<int:noticia_id>/', views.detalhar_noticia, name='detalhar_noticia'),
    path('noticias/editar_noticia/<int:noticia_id>/', views.editar_noticia, name='editar_noticia'),

#polos
    path('polos/',views.polos_lista, name="polo_lista"),
    path('criar_polo/', views.criar_polo, name='criar_polo'),
    path('vincular_polo/', views.vincular_curso_polo, name='vincular_polo'),
    path('excluir_polo/<int:polo_id>/', views.excluir_polo, name='excluir_polo'),
    path('detalhar_polo/<int:polo_id>/', views.detalhar_polo, name='detalhar_polo'),
    path('editar_polo/<int:polo_id>/', views.editar_polo, name='editar_polo'),

#coordenadores
    path('coordenadores/',views.coordenadores_lista, name="coordenador_lista"),
    path('criar_coordenador/', views.criar_coordenador, name='criar_coordenador'),
    path('vincular_coordenador/', views.vincular_curso_coordenador, name='vincular_coordenador'),
    path('excluir_coordenador/<int:coordenador_id>/', views.excluir_coordenador, name='excluir_coordenador'),
    path('detalhar_coordenador/<int:coordenador_id>/', views.detalhar_coordenador, name='detalhar_coordenador'),
    path('editar_coordenador/<int:coordenador_id>/', views.editar_coordenador, name='editar_coordenador'),

#mediadores
    path('mediadores/',views.mediadores_lista, name="mediador_lista"),
    path('criar_mediador/', views.criar_mediador, name='criar_mediador'),
    path('vincular_mediador/', views.mediacao, name='vincular_mediador'),
    path('excluir_mediador/<int:mediador_id>/', views.excluir_mediador, name='excluir_mediador'),
    path('detalhar_mediador/<int:mediador_id>/', views.detalhar_mediador, name='detalhar_mediador'),
    path('editar_mediador/<int:mediador_id>/', views.editar_mediador, name='editar_mediador'),

#curso
    path('curso/',views.curso_lista, name="curso_lista"),
    path('criar_curso/', views.criar_curso, name='criar_curso'),
    path('vincular_curso/', views.vincular_curso, name='vincular_curso'),
    path('detalhar_curso/<int:coordenador_id>/<int:curso_id>/', views.detalhar_curso, name='detalhar_curso'),
    path('excluir_cursoPolo/<int:cursoPolo_id>/', views.excluir_cursoPolo, name='excluir_cursoPolo'),
    path('detalhar_cursoPolo/<int:cursoPolo_id>/', views.detalhar_cursoPolo, name='detalhar_cursoPolo'),

#disciplina
    path('disciplina/',views.disciplina_lista, name="disciplina_lista"),
    path('criar_disciplina/', views.criar_disciplina, name='criar_disciplina'),
    path('vincular_disciplina/', views.vincular_disciplina, name='vincular_disciplina'),
    path('detalhar_disciplina/<int:curso_id>/', views.detalhar_disciplina, name='detalhar_disciplina'),
    path('excluir_disciplina/<int:disciplina_id>/', views.excluir_disciplina, name='excluir_disciplina'),
    path('detalhar_disciplina/<int:disciplina_id>/', views.detalhar_disciplina, name='detalhar_disciplina'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

