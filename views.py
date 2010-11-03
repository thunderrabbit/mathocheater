from django.shortcuts import render_to_response
from forms import DigitsForm
from models import Digits, Answers, Statistics
import datetime

def index(request):

    four_digits = 0
    empty_form = DigitsForm()
    
    if(request.GET.__contains__('digits')):
        four_digits = request.GET['digits']
    
    if(four_digits):
        template_name = 'solved.html'

        incoming_form = DigitsForm({'digits':four_digits})
        if(incoming_form.is_valid() and len(four_digits) == 4):
            d1 = request.GET['digits'][0];
            d2 = request.GET['digits'][1];
            d3 = request.GET['digits'][2];
            d4 = request.GET['digits'][3];

            answer = Answers.objects.filter(digits__d1__exact=d1,digits__d2__exact=d2,digits__d3__exact=d3,digits__d4__exact=d4).values('solution','digits_id')
            if(answer):
                solution = answer[0]['solution']  # thanks to Denis G./M/Volgograd,RussianFederation for this syntax  (2 November 2010)
                digits_id = answer[0]['digits_id']  # will be used to pull statistics item

                # begin code that updates counter for this already-saved Digits item
                statistic = Statistics.objects.filter(digits=digits_id)
                if(statistic):
                    pass
                else:
                    update_digits_count = Digits.objects.get(id=digits_id)
                    update_digits_count.counter += 1
                    update_digits_count.save()
            else:
                digits = Digits(d1 = d1, d2 = d2, d3=d3, d4=d4, counter=1)
                answer = digits.solve()
                solution = answer.solution

            if(solution != 'none'):
                solution = solution + " = " + str(eval(solution))
            return render_to_response(template_name, {'form':empty_form, 'solution':solution})

        else:
            return render_to_response(template_name, {'form':incoming_form})
    else:
        template_name = 'index.html'
        return render_to_response(template_name, {'form':empty_form})


def statistics(request):
    answers = Answers.objects.all().order_by('-digits__counter')
    return render_to_response("statistics.html",{'answers':answers})
    
