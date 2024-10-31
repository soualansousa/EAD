from django.urls import path
from . import views
app_name= 'app'

urlpatterns = [
    path('',views.user_login, name="login"),
    path('home_cead/',views.home_cead, name="home_cead"),
    path('home_coo/',views.home_coo, name="home_coo"),
    path('noticias/',views.noticias),
]