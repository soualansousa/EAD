from django import forms
from .models import Noticia, Polo

class SearchForm(forms.Form):
    query = forms.CharField(label="Buscar", max_length=100, required=False)

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['curso', 'titulo', 'descricao']

class PoloForm(forms.ModelForm):
    class Meta:
        model = Polo
        fields = ['curso', 'coordenador', 'cidade', 'latitude', 'longitude']