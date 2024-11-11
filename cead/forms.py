from django import forms
from .models import Noticia, Polo, Coordenador

class SearchForm(forms.Form):
    query = forms.CharField(label="Buscar", max_length=100, required=False)

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['curso', 'titulo', 'descricao']

class PoloForm(forms.ModelForm):
    class Meta:
        model = Polo
        fields = ['coordenador', 'cidade', 'latitude', 'longitude']

class CoordenadorForm(forms.ModelForm):
    class Meta:
        model = Coordenador
        fields = ['nome', 'email', 'telefone', 'situacao']