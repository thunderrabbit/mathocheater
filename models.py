from django.db import models
import re

class Digits (models.Model):
    """Basically stores 4 digits and knows how to run through permutations of operators 
    (including parenthesis) to figure out a combination that equals 10.

    Eventually will increment the counter each time a set of 4 digits is processed, but that's not
    written yet until I set up a table to block repeats by the same IP address in short time span."""

    d1 = models.IntegerField()
    d2 = models.IntegerField()
    d3 = models.IntegerField()
    d4 = models.IntegerField()
    counter = models.IntegerField()   # unique requests for this set of digits

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

        # force floating point math by adding ".0" to end of each digit
        d1 = str(self.d1) + ".0"
        d2 = str(self.d2) + ".0"
        d3 = str(self.d3) + ".0"
        d4 = str(self.d4) + ".0"

        #-------------------------------------------------------------------#
        #
        #  this begins a brute force process of evaluating all the possible
        #  permutations of equations until it finds one that equals 10, or
        #  finds none equal 10.
        #
        #------------------------------------------------------------------#
        for parenthesis_option in parenthesis_options:
            self.set_parenthesis(parenthesis_option)
            for o1 in operators:
                for o2 in operators:
                    for o3 in operators:
                        result_float_string = self.paren1 + d1 + o1 + self.paren2 + d2 + self.paren3 + o2 + self.paren4 + d3 + self.paren5 + o3 + d4 + self.paren6
                        try:
                            result_int = eval(result_float_string)
                        except ZeroDivisionError:
                            result_int = 0
                        if(result_int == 10):
                            # remove ".0" from each number to make them whole digits
                            result_string = re.sub(r'\.0','',result_float_string)
                            finished = 1
                            break
                    if(finished):
                        break
                if(finished):
                    break
            if(finished):
                break

        self.save()
        self.log()
        if(finished):
            answer = self.answers_set.create(solution = result_string)
        else:
            answer = self.answers_set.create(solution = 'none')
        return answer

    def log(self):

        ''' creates statistic item and  updates counter '''
        #  I'm thinking if it's the same IP address during the same date,
        #  do *not* count it.
        statistic = Statistics.objects.filter(digits=self.id)    # should filter on IP address and date as well
        if(statistic):
            statistic[0].counter += 1    # this is counted as a reloaded item (ballot stuffing)
            statistic[0].save()
        else:
            self.statistics_set.create(IP='dog',counter=1)  #  need to store the IP address
            self.counter += 1
            self.save()



    

    def set_parenthesis(self, p_option):
        self.paren1 = self.paren2 = self.paren3 = self.paren4 = self.paren5 = self.paren6 = ""
        if(p_option == 'none'):
            pass
        elif(p_option == 'first pair'):
            # (A + B) + C + D
            self.paren1 = '('
            self.paren3 = ')'
        elif(p_option == 'second pair'):
            # A + (B + C) + D
            self.paren2 = '('
            self.paren5 = ')'
        elif(p_option == 'third pair'):
            # A + B + (C + D)
            self.paren4 = '('
            self.paren6 = ')'
        elif(p_option == 'both pairs'):
            # (A + B) + (C + D)
            self.paren1 = '('
            self.paren3 = ')'
            self.paren4 = '('
            self.paren6 = ')'
        elif(p_option == 'first three'):
            # (A + B + C) + D
            self.paren1 = '('
            self.paren5 = ')'
        elif(p_option == 'last three'):
            # A + (B + C + D)
            self.paren2 = '('
            self.paren6 = ')'

class Answers (models.Model):
    ''' stores an answer for a set of digits or 'none' if none exists '''
    digits = models.ForeignKey(Digits)
    solution = models.CharField(max_length=20)
    def __unicode__(self):
        try:
            response = self.solution + " = " +  str(eval(self.solution))
        except:
            response = "no solution found"
        return response

class Statistics (models.Model):
    """ stores unique hits for Digits
    The query is considered unique if:
    
    different Digits     OR
    different IP address OR
    different day"""

    digits = models.ForeignKey(Digits)
    IP = models.CharField(max_length=40)
    counter = models.IntegerField()  # repeated requests for these digits from this IP address on this date
    created_on = models.DateField(auto_now = False, auto_now_add = True)
    updated_on = models.DateField(auto_now = True, auto_now_add = False)

