from django.db import models
import re

# Create your models here.

class Digits (models.Model):
    d1 = models.IntegerField()
    d2 = models.IntegerField()
    d3 = models.IntegerField()
    d4 = models.IntegerField()
    counter = models.IntegerField()  # deprecated

    def __unicode__(self):
        return str(self.d1) + " " + str(self.d2) + " " + str(self.d3) + " " + str(self.d4)

    def solve(self):
        operators = ['+', '-', '*',  '/']
        parenthesis_options = ['none', 'first pair', 'second pair', 'third pair', 'both pairs', 'first three', 'last three']

        finished = 0
        operator1 = operator2 = operator3 = ""
        paren1 = paren2 = paren3 = paren4 = paren5 = paren6 = ""

        result_string = ""
        result_float_string = ""
        result_int = 0
        for parenthesis_option in parenthesis_options:
            self.set_parenthesis(parenthesis_option)
            for o1 in operators:
                for o2 in operators:
                    for o3 in operators:
                        result_string = self.paren1 + str(self.d1) + o1 + self.paren2 + str(self.d2) + self.paren3 + o2 + self.paren4 + str(self.d3) + self.paren5 + o3 + str(self.d4) + self.paren6
                        # force floating point math by adding ".0" to end of each digit
                        result_float_string = re.sub(r'(\d)',r'\1.0',result_string)
                        try:
                            result_int = eval(result_float_string)
                        except ZeroDivisionError:
                            result_int = 0
                        if(result_int == 10):
                            finished = 1
                            break
                    if(finished):
                        break
                if(finished):
                    break
            if(finished):
                break

        self.save()
        if(finished):
            answer = self.answers_set.create(solution = result_string)
        else:
            answer = self.answers_set.create(solution = str(self.d1) + " ? " + str(self.d2) + " ? " + str(self.d3) + " ? " + str(self.d4))
        return answer

    def set_parenthesis(self, p_option):
        self.paren1 = self.paren2 = self.paren3 = self.paren4 = self.paren5 = self.paren6 = ""
        if(p_option == 'none'):
            pass
        elif(p_option == 'first pair'):
            self.paren1 = '('
            self.paren3 = ')'
        elif(p_option == 'second pair'):
            self.paren2 = '('
            self.paren5 = ')'
        elif(p_option == 'third pair'):
            self.paren4 = '('
            self.paren6 = ')'
        elif(p_option == 'both pairs'):
            self.paren1 = '('
            self.paren3 = ')'
            self.paren4 = '('
            self.paren6 = ')'
        elif(p_option == 'first three'):
            self.paren1 = '('
            self.paren5 = ')'
        elif(p_option == 'last three'):
            self.paren2 = '('
            self.paren6 = ')'

            
class Answers (models.Model):
    digits = models.ForeignKey(Digits)
    solution = models.CharField(max_length=20)
    def __unicode__(self):
        try:
            response = self.solution + " = " +  str(eval(self.solution))
        except:
            response = "no solution found"
        return response
