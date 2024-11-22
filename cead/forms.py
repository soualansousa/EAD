from django import forms

from .models import Noticia, Polo, Coordenador, Curso, Mediador, Gestor

from .models import Noticia, Polo, Coordenador, Curso, Mediador, CoordenadorCurso


class SearchForm(forms.Form):
    query = forms.CharField(label="Buscar", max_length=100, required=False)

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['curso', 'titulo', 'descricao', 'arquivo']

class PoloForm(forms.ModelForm):
    class Meta:
        model = Polo
        fields = ['coordenador', 'cidade', 'latitude', 'longitude']

class CoordenadorForm(forms.ModelForm):
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        required=False,
        label="Curso",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Coordenador
        fields = ['nome', 'email', 'telefone']

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        curso = self.cleaned_data.get('curso')
        if curso:
            CoordenadorCurso.objects.update_or_create(
                coordenador=instance,
                defaults={'curso': curso}
            )

        return instance

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['coordenador', 'nome', 'sobre',]

class MediadorForm(forms.ModelForm):
    class Meta:
        model = Mediador
        fields = ['curso_polo', 'nome', 'email', 'telefone', 'formacao', 'situacao']

class GestorForm(forms.ModelForm):
    class Meta:
        model = Gestor
        fields = ['nome', 'email', 'telefone', 'formacao', 'situacao']
