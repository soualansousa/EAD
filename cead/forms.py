from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label="Buscar", max_length=100, required=False)