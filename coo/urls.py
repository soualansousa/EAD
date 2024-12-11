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

#disciplina
    path('disciplina/',views.disciplina_lista, name="disciplina_lista"),
    path('criar_disciplina/', views.criar_disciplina, name='criar_disciplina'),
    # path('disciplina/detalhar_disciplina/<int:disciplina_id>/', views.detalhar_disciplina, name='detalhar_disciplina'),
    # path('disciplina/excluir_disciplina/<int:disciplina_id>/', views.excluir_disciplina, name='excluir_disciplina'),
    # path('disciplina/detalhar_disciplina/<int:disciplina_id>/', views.detalhar_disciplina, name='detalhar_disciplina'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






