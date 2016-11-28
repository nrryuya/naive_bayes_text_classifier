from django.forms import ModelForm
from django import forms
from cms.models import Article


class ArticleForm(ModelForm):
    """記事のフォーム"""
    class Meta:
        model = Article
        fields = ('title', 'url', 'category', )
        
class UrlForm(forms.Form):
    article_url =  forms.CharField(
        label='URL',
        max_length=255,
        required=True,
        widget=forms.TextInput()
    )