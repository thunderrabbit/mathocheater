from django.conf.urls.defaults import *

urlpatterns = patterns('mathoholic.mathocheater.views',
    (r'^$', 'index'),
    (r'^(?P<d1>\d)[^\d]?(?P<d2>\d)[^\d]?(?P<d3>\d)[^\d]?(?P<d4>\d)[^\d]?$', 'solve')
)
