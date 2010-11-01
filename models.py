from django.db import models

# Create your models here.

class Digits (models.Model):
    d1 = models.IntegerField()
    d2 = models.IntegerField()
    d3 = models.IntegerField()
    d4 = models.IntegerField()
    counter = models.IntegerField()
    def __unicode__(self):
        return str(self.d1) + " " + str(self.d2) + " " + str(self.d3) + " " + str(self.d4)

class Answers (models.Model):
    digits = models.ForeignKey(Digits)
    solution = models.CharField(max_length=20)
    def __unicode__(self):
        return self.solution + " = " + str(eval(self.solution))
