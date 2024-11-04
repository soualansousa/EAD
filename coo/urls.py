from django.urls import path
from . import views
app_name= 'coo'

urlpatterns = [
    path('coordenacao/',views.coordenacao, name="coordenacao"),
]