from django.db import models

class Noticia(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, editable=False)
    Título = models.CharField(max_length=65)
    Descrição = models.TextField(max_length=165)
    Data_pub = models.DateTimeField(auto_now_add=True)
    Data_mod = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Título