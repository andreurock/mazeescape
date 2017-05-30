from django.db import models

class Name(models.Model):
    name = models.TextField()
    email = models.TextField()
