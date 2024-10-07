from django.db import models

class phone(models.Model):
    nom = models.CharField(max_length=100)
    lien = models.TextField()
    marque = models.CharField(max_length=50)
    prix = models.FloatField()
    image = models.CharField(max_length=100)

    def __str__(self):
        return self.nom