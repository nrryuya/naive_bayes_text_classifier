from django.db import models
from django.conf import settings

# Create your models here.
class Article(models.Model):
    """記事"""
    title = models.CharField('タイトル', max_length=255, default='title')
    url = models.CharField('URL', max_length=255)
    category = models.CharField('カテゴリー', max_length=255, blank=True)
    
    def __str__(self):
        return self.title
    
    