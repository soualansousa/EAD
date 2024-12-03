from django import forms

from .models import Noticia, Polo, Coordenador, Curso, Mediador, Gestor

from .models import Noticia, Polo, Coordenador, Curso, Mediador, CoordenadorCurso, NoticiaCurso, CursoPolo, Mediacao, GestorPolos


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
        required=True,
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
        required=True,
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
    coordenador = forms.ModelChoiceField(
        queryset=Coordenador.objects.all(),
        required=False,
        label="Coordenador",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Curso
        fields = ['nome', 'sobre',]

class CoordenadorCursoForm(forms.ModelForm):
    class Meta:
        model = CoordenadorCurso
        fields = ['coordenador', 'curso', 'saida']

class MediadorForm(forms.ModelForm):
    modalidade = forms.ChoiceField(
        choices=Mediacao.MODALIDADE_CHOICES,
        required=True,
        label="Modalidade",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    curso_polos = forms.ModelChoiceField(
        queryset=CursoPolo.objects.all(),
        required=True,
        label="Curso - Polo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    saida = forms.DateField(
        required=False,
        label="Data de Saída",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    class Meta:
        model = Mediador
        fields = ['nome', 'email', 'telefone', 'formacao']

    def __init__(self, *args, **kwargs):
        self.mediacao = kwargs.pop('mediacao', None)
        curso_polos_id = kwargs.pop('curso_polos_id', None)
        super().__init__(*args, **kwargs)

        if curso_polos_id:
            self.fields['curso_polos'].initial = CursoPolo.objects.get(id=curso_polos_id)

        if self.mediacao:
            self.fields['saida'].initial = self.mediacao.saida
            self.fields['modalidade'].initial = self.mediacao.modalidade

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        modalidade = self.cleaned_data.get('modalidade')
        curso_polos = self.cleaned_data.get('curso_polos')
        saida = self.cleaned_data.get('saida')

        if self.mediacao:
            self.mediacao.curso_polos = curso_polos
            self.mediacao.saida = saida
            self.mediacao.modalidade = modalidade
            self.mediacao.save()
        else:
            Mediacao.objects.create(
                mediador=instance,
                curso_polos=curso_polos,
                modalidade=modalidade,
                saida=saida,
            )

        return instance

class GestorForm(forms.ModelForm):
    saida = forms.DateField(
        required=False,
        label="Data de Saída",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Gestor
        fields = ['nome', 'email', 'telefone', 'formacao', 'situacao']

    def __init__(self, *args, **kwargs):
        self.gestor = kwargs.pop('gestor', None)
        super().__init__(*args, **kwargs)

        if self.gestor:
            self.fields['saida'].initial = self.gestor.saida

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        # Trata o campo 'saida' separadamente
        saida = self.cleaned_data.get('saida')
        if self.gestor:
            self.gestor.saida = saida
            self.gestor.save()

        return instance        
    
