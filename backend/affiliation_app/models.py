from django.db import models

# Create your models here.
class Affiliation(models.Model):
    category = models.CharField(max_length=50, unique=True)