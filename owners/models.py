from django.db import models

# Create your models here.


class Owners(models.Model):
    name = models.Charfield()