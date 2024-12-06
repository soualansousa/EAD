from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name= 'coo'

urlpatterns = [
    path('coordenacao/',views.coordenacao, name="coordenacao"),



#curso
    path('curso/',views.curso_lista_coo, name="curso_lista_coo"),
    path('criar_curso/', views.criar_curso, name='criar_curso'),
    path('vincular_curso/', views.vincular_curso, name='vincular_curso'),
    path('detalhar_curso/<int:coordenador_id>/<int:curso_id>/', views.detalhar_curso, name='detalhar_curso'),
    path('excluir_cursoPolo/<int:cursoPolo_id>/', views.excluir_cursoPolo, name='excluir_cursoPolo'),
    path('detalhar_cursoPolo/<int:cursoPolo_id>/', views.detalhar_cursoPolo, name='detalhar_cursoPolo'),

#notícias
    path('noticias/',views.noticias_lista, name="noticia_lista"),
    path('criar_noticia/', views.criar_noticia, name='criar_noticia'),
    path('excluir_noticia/<int:noticia_id>/', views.excluir_noticia, name='excluir_noticia'),
    path('detalhar_noticia/<int:noticia_id>/', views.detalhar_noticia, name='detalhar_noticia'),
    path('editar_noticia/<int:noticia_id>/', views.editar_noticia, name='editar_noticia'),

#mediadores
    path('mediadores/',views.mediadores_lista, name="mediador_lista"),
    path('criar_mediador/', views.criar_mediador, name='criar_mediador'),
    path('vincular_mediador/', views.mediacao, name='vincular_mediador'),
    path('excluir_mediador/<int:mediador_id>/', views.excluir_mediador, name='excluir_mediador'),
    path('detalhar_mediador/<int:mediador_id>/', views.detalhar_mediador, name='detalhar_mediador'),
    path('editar_mediador/<int:mediador_id>/', views.editar_mediador, name='editar_mediador'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






