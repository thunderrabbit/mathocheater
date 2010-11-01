from django.http import HttpResponse
from models import Digits, Answers

def index(request):
    return HttpResponse("Hello, world. You're at the Mathoholic Cheater index.")

def solve(request, d1, d2, d3, d4):
    answer = Answers.objects.filter(digits__d1__exact=d1,digits__d2__exact=d2,digits__d3__exact=d3,digits__d4__exact=d4)
    if(answer):
        output = answer
    else:
        digits = Digits(d1 = d1, d2 = d2, d3=d3, d4=d4, counter=0)
        answer = digits.solve()
        output = answer

    return HttpResponse(output)
