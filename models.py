from django.db import models

# Create your models here.

class Digits (models.Model):
    d1 = models.IntegerField()
    d2 = models.IntegerField()
    d3 = models.IntegerField()
    d4 = models.IntegerField()
    counter = models.IntegerField()

class Answers (models.Model):
    digits = models.ForeignKey(Digits)
    solution = models.CharField(max_length=20)
