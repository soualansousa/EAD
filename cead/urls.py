from django.urls import path
from . import views
app_name= 'cead'

urlpatterns = [
    path('',views.user_login, name="login"),
    path('cead/',views.cead, name="cead"),

#notícias
    path('noticias/',views.noticias_lista, name="noticia_lista"),
    path('criar_noticia/', views.criar_noticia, name='criar_noticia'),
    path('excluir_noticia/<int:noticia_id>/', views.excluir_noticia, name='excluir_noticia'),
    path('detalhar_noticia/<int:noticia_id>/', views.detalhar_noticia, name='detalhar_noticia'),
    path('editar_noticia/<int:noticia_id>/', views.editar_noticia, name='editar_noticia'),

#polos
    path('polos/',views.polos_lista, name="polo_lista"),
    path('criar_polo/', views.criar_polo, name='criar_polo'),
    path('excluir_polo/<int:polo_id>/', views.excluir_polo, name='excluir_polo'),
    path('detalhar_polo/<int:polo_id>/', views.detalhar_polo, name='detalhar_polo'),
    path('editar_polo/<int:polo_id>/', views.editar_polo, name='editar_polo'),


#coordenadores
    path('coordenadores/',views.coordenadores_lista, name="coordenador_lista"),
    path('criar_coordenador/', views.criar_coordenador, name='criar_coordenador'),
    path('excluir_coordenador/<int:coordenador_id>/', views.excluir_coordenador, name='excluir_coordenador'),
    path('detalhar_coordenador/<int:coordenador_id>/', views.detalhar_coordenador, name='detalhar_coordenador'),
    path('editar_coordenador/<int:coordenador_id>/', views.editar_coordenador, name='editar_coordenador'),
]