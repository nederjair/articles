from django import forms
from django.forms import ModelForm
from .models import Article

class QuoteForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Article
        fields = [
            'title', 
        ]

class SearchForm(forms.Form):
    query = forms.CharField()
