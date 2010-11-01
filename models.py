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

    def solve(self):
        operators = ['+', '-', '*',  '/']

        operator1 = operator2 = operator3 = ""

        for o1 in operators:
            for o2 in operators:
                for o3 in operators:
                    try:
                        result = eval(str(self.d1) + o1 + str(self.d2) + o2 + str(self.d3) + o3 + str(self.d4))
                    except ZeroDivisionError:
                        result = 0
                    if(result == 10):
                        operator1 = o1
                        operator2 = o2
                        operator3 = o3
                        break
                if(operator3):
                    break
            if(operator3):
                break

        self.save()
        if(len(operator3)):
            answer = self.answers_set.create(solution = str(self.d1) + operator1 + str(self.d2) + operator2 + str(self.d3) + operator3 + str(self.d4))
        else:
            answer = self.answers_set.create(solution = str(self.d1) + " ? " + str(self.d2) + " ? " + str(self.d3) + " ? " + str(self.d4))
        return answer

class Answers (models.Model):
    digits = models.ForeignKey(Digits)
    solution = models.CharField(max_length=20)
    def __unicode__(self):
        try:
            response = self.solution + " = " +  str(eval(self.solution))
        except:
            response = "no solution found"
        return response
