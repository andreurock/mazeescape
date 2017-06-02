from django.db import models


class Wall(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()


class Game(models.Model):
    gameId = models.TextField()
