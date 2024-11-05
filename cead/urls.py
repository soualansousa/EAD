from django.urls import path
from . import views
app_name= 'cead'

urlpatterns = [
    path('',views.user_login, name="login"),
    path('cead/',views.cead, name="cead"),
    path('noticias/',views.noticias_lista, name="noticia_lista"),
    path('polos/',views.polos_lista, name="polo_lista"),
]