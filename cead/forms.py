from django import forms

from .models import Noticia, Polo, Coordenador, Curso, Mediador, Gestor

from .models import Noticia, Polo, Coordenador, Curso, Mediador, CoordenadorCurso, NoticiaCurso


class SearchForm(forms.Form):
    query = forms.CharField(label="Buscar", max_length=100, required=False)

class NoticiaForm(forms.ModelForm):
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        required=False,
        label="Curso",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Noticia
        fields = ['titulo', 'descricao', 'arquivo']

    def __init__(self, *args, **kwargs):
        self.noticia_curso = kwargs.pop('noticia_curso', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        curso = self.cleaned_data.get('curso')

        if self.noticia_curso:
            self.noticia_curso.curso = curso
            self.noticia_curso.save()
        else:
            NoticiaCurso.objects.create(
                noticia=instance,
                curso=curso,
            )

        return instance

class PoloForm(forms.ModelForm):

    gestor = forms.ModelChoiceField(
        queryset=Gestor.objects.all(),
        required=False,
        label="Gestor",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    saida = forms.DateField(
        required=False,
        label="Data de Saída",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Polo
        fields = ['cidade', 'longitude', 'latitude']

    def __init__(self, *args, **kwargs):
        self.gestor_polos = kwargs.pop('gestor_polos', None)
        super().__init__(*args, **kwargs)

        if self.gestor_polos:
            self.fields['saida'].initial = self.gestor_polos.saida

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        gestor = self.cleaned_data.get('gestor')
        saida = self.cleaned_data.get('saida')

        if self.gestor_polos:
            self.gestor_polos.gestor = gestor
            self.gestor_polos.saida = saida
            self.gestor_polos.save()
        else:
            GestorPolos.objects.create(
                polo=instance,
                gestor=gestor,
                saida=saida,
            )

        return instance

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
                saida=saida,
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
