from django.core.paginator import Paginator, InvalidPage, EmptyPage
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
            digits = Digits(digits = four_digits, counter = 0)

            answers = Answers.objects.filter(digits__digits__exact = four_digits)
            if(answers):
                answers[0].digits.log(request)  # thanks to Denis G./M/Volgograd,RussianFederation for this syntax
            else:
                digits.save()
                digits.log(request)
                digits.solve()
                answers = Answers.objects.filter(digits__digits__exact = four_digits)
            return render_to_response(template_name, {'form':empty_form, 'answers':answers})
        else:
            # there was an input error
            return render_to_response(template_name, {'form':incoming_form})
    else:
        # no digits sent
        template_name = 'index.html'
        return render_to_response(template_name, {'form':empty_form})


def statistics(request):
    sort_by = request.GET.get('by', 'counter')
    sort_dir = request.GET.get('dir', 'descending')

    dir_dic = {'descending':'-','ascending':''}
    dir_dic_keys = dir_dic.keys();
    if(sort_by not in ['digits', 'answers', 'counter']):
        sort_by = 'counter'
    if(sort_dir not in dir_dic_keys):
        sort_dir = 'descending'

    dir_dic_keys.remove(sort_dir)
    other_sort_direction = dir_dic_keys[0]
    
    answer_list = Answers.objects.all().order_by(dir_dic[sort_dir] + 'digits__' + sort_by)
    paginator = Paginator(answer_list, 15, 5)  # Show 15 answers per page, at least 5 (and less than 20) on the last page

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request is an int, but the page DNE, go with the last page
    try:
        answers = paginator.page(page)
    except (EmptyPage, InvalidPage):
        answers = paginator.page(paginator.num_pages)
        
                            
    return render_to_response("statistics.html",{'answers':answers,'other_sort_direction':other_sort_direction})
    
