from django.shortcuts import render_to_response
from forms import DigitsForm
from models import Digits, Answers
import datetime

def index(request):
    form = DigitsForm()
    return render_to_response('index.html', {'form':form})

def solve(request, d1, d2, d3, d4):
    form = DigitsForm({'digits':934})
    if(form.is_valid()):
        answer = Answers.objects.filter(digits__d1__exact=d1,digits__d2__exact=d2,digits__d3__exact=d3,digits__d4__exact=d4).values('solution')
        if(answer):
            solution = answer[0]['solution']  # thanks to Denis G./M/Volgograd,RussianFederation for this syntax
        else:
            digits = Digits(d1 = d1, d2 = d2, d3=d3, d4=d4, counter=0)
            answer = digits.solve()
            solution = answer.solution
    else:
        return render_to_response('solved.html', {'form':form})
    return render_to_response('solved.html', {'form':form, 'answer':solution})
