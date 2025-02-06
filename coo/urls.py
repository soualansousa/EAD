from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name= 'coo'

urlpatterns = [
    path('',views.coordenacao, name="coordenacao"),

#curso
    path('curso/',views.curso_lista_coo, name="curso_lista_coo"),

#notícias
    path('noticias/',views.noticias_lista, name="noticia_lista"),
    path('criar_noticia/', views.criar_noticia, name='criar_noticia'),
    path('noticias/excluir_noticia/<int:noticia_id>/', views.excluir_noticia, name='excluir_noticia'),
    path('noticias/detalhar_noticia/<int:noticia_id>/', views.detalhar_noticia, name='detalhar_noticia'),
    path('noticias/editar_noticia/<int:noticia_id>/', views.editar_noticia, name='editar_noticia'),

#mediadores
    path('mediadores/',views.mediadores_lista, name="mediador_lista"),
    path('criar_mediador/', views.criar_mediador, name='criar_mediador'),
    path('vincular_mediador/', views.mediacao, name='vincular_mediador'),
    path('mediadores/excluir_mediador/<int:mediador_id>/', views.excluir_mediador, name='excluir_mediador'),
    path('mediadores/detalhar_mediador/<int:mediador_id>/', views.detalhar_mediador, name='detalhar_mediador'),
    path('mediadores/editar_mediador/<int:mediador_id>/', views.editar_mediador, name='editar_mediador'),

#disciplina
    path('disciplina/',views.disciplina_lista, name="disciplina_lista"),
    path('criar_disciplina/', views.criar_disciplina, name='criar_disciplina'),
    path('editar_disciplina/<int:disciplina_id>/', views.editar_disciplina, name='editar_disciplina'),
    path('excluir_disciplina/<int:disciplina_id>/', views.excluir_disciplina, name='excluir_disciplina'),
    path('detalhar_disciplina/<int:disciplina_id>/', views.detalhar_disciplina, name='detalhar_disciplina'),

#contato
    path('contato/',views.contato_lista, name="contato_lista"),
    path('criar_contato/', views.criar_contato, name='criar_contato'),
    path('editar_contato/<int:contato_id>/', views.editar_contato, name='editar_contato'),
    path('excluir_contato/<int:contato_id>/', views.excluir_contato, name='excluir_contato'),
    path('detalhar_contato/<int:contato_id>/', views.detalhar_contato, name='detalhar_contato'),

#contato_publico
    path('contato_publico/', views.contato_publico, name='contato_publico'),
    path('enviar_contato/', views.enviar_contato, name='enviar_contato'),


#teste
    path('teste/', views.pagina_teste, name='pagina_teste'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






