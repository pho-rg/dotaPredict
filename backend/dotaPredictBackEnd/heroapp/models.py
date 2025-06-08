from django.db import models

# Create your models here.
class Hero(models.Model):
    hero_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)