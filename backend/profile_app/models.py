from django.db import models
from django.core import validators as v
from user_app.models import User
from affiliation_app.models import Affiliation

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    display_name = models.CharField(validators=[v.MinLengthValidator(3), v.MaxLengthValidator(50)], null=True, blank=True)
    affiliations = models.ManyToManyField(Affiliation, related_name='affiliations', blank=True)