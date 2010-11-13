from django.http import HttpResponse
from django.db import models
import re, datetime

class Digits (models.Model):
    """
    Basically stores 4 digits and knows how to run through permutations of operators 
    (including parenthesis) to find combinations that equal 10
    """

    digits = models.CharField(max_length=4)
    counter = models.IntegerField()   # unique requests for this set of digits

    def __unicode__(self):
        return self.digits

    def solve(self):
        """
        Brute force through all combinations of operators and parenthesis, recording all the results that equal 10
        simplest solutions are tried first

        TODO:  discard solutions that are simply adding parenthesis
            5 + 5 + 5 + 5 = 10  good
           (5 + 5)+(5 + 5)= 10  don't care
        """
        operators = ['+', '-', '*',  '/']
        parenthesis_options = ['none', 'first pair', 'second pair', 'third pair', 'both pairs', 'first three', 'last three']

        operator1 = operator2 = operator3 = ""
        paren1 = paren2 = paren3 = paren4 = paren5 = paren6 = ""

        result_string = ""
        result_float_string = ""
        result_int = 0
        solution_found = False

        # force floating point math by adding ".0" to end of each digit
        d1 = self.digits[0] + ".0"
        d2 = self.digits[1] + ".0"
        d3 = self.digits[2] + ".0"
        d4 = self.digits[3] + ".0"

        answers = []
        self.save()

        #-------------------------------------------------------------------#
        #                                                                   #
        #  this begins a brute force process of evaluating all the possible #
        #  permutations of equations until it finds one that equals 10, or  #
        #  finds none equal 10.                                             #
        #                                                                   #
        #-------------------------------------------------------------------#
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
                            self.answers_set.create(solution = result_string)
                            solution_found = True

        if(not solution_found):
            self.answers_set.create(solution = 'none')

    def log(self,request):
        """
        creates statistic item and  updates counter
        """
        #  I'm thinking if it's the same IP address during the same date,
        #  do *not* count it.
        ip_address = request.META['REMOTE_ADDR']  # request.META['HTTP_X_FORWARDED_FOR']
        todays_date = datetime.date.today()
        statistic = Statistics.objects.filter(digits=self.id,IP=ip_address,updated_on=todays_date)
        if(statistic):
            statistic[0].counter += 1    # this is counted as a reloaded item (ballot stuffing)
            statistic[0].save()
        else:
            self.statistics_set.create(IP=ip_address,counter=1)  #  need to store the IP address
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
    """
    stores an answer for a set of digits or 'none' if none exists
    """
    digits = models.ForeignKey(Digits)
    solution = models.CharField(max_length=20)
    def __unicode__(self):
        if(self.solution == 'none'):
            response = "no solution found"
        else:
            float_string = re.sub(r'(\d)',r'\1.0',self.solution)                            # add .0 to digits to force floating point math
            response = self.solution + " = " +  re.sub(r'\.0','',str(eval(float_string)))   # remove .0 from answer to make it look right
        return response

    def beautify(self,answers_queryset):
        """
        process set of solutions before sending to template
        """
        prev_digits = ""
        output = []
        for answer in answers_queryset:
            if prev_digits != answer.digits.digits:
                prev_digits = answer.digits.digits
                output.append({'four_digits':prev_digits,'count':answer.digits.counter})
            output.append({'answer':answer.solution})
        return(output)

class Statistics (models.Model):
    """
    Stores unique hits for Digits
    The query is considered unique if:
    
    different Digits     OR
    different IP address OR
    different day
    """

    digits = models.ForeignKey(Digits)
    IP = models.CharField(max_length=40)
    counter = models.IntegerField()  # repeated requests for these digits from this IP address on this date
    created_on = models.DateField(auto_now = False, auto_now_add = True)
    updated_on = models.DateField(auto_now = True, auto_now_add = False)

