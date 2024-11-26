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
    gestor = forms.ModelChoiceField(
        queryset=Gestor.objects.all(),
        required=False,
        label="Gestor",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class CoordenadorForm(forms.ModelForm):
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        required=False,
        label="Curso",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    saida = forms.DateField(
        required=False,
        label="Data de Saída",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Coordenador
        fields = ['nome', 'email', 'telefone']

    def __init__(self, *args, **kwargs):
        self.coordenador_curso = kwargs.pop('coordenador_curso', None)
        super().__init__(*args, **kwargs)

        if self.coordenador_curso:
            self.fields['saida'].initial = self.coordenador_curso.saida

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        curso = self.cleaned_data.get('curso')
        saida = self.cleaned_data.get('saida')

        if self.coordenador_curso:
            self.coordenador_curso.curso = curso
            self.coordenador_curso.saida = saida
            self.coordenador_curso.save()
        else:
            CoordenadorCurso.objects.create(
                coordenador=instance,
                curso=curso,
                saida=saida
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
