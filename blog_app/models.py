from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
