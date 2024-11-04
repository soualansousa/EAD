from django.urls import path
from . import views
app_name= 'cead'

urlpatterns = [
    path('',views.user_login, name="login"),
    path('home_cead/',views.home_cead, name="home_cead"),
    path('home_coo/',views.home_coo, name="home_coo"),
    path('noticias/',views.noticias_lista, name="noticia_lista"),
    path('noticias/<int:id>/', views.visualizar_noticia, name='visualizar_noticia'),
    path('noticias/editar/<int:id>/', views.editar_noticia, name='editar_noticia'),
    path('noticias/remover/<int:id>/', views.remover_noticia, name='remover_noticia'),
]