from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('viewer', 'Viewer'),
        ('analyst', 'Analyst'),
    ]

    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=256)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')