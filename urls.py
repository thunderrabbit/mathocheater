from django.conf.urls.defaults import *

urlpatterns = patterns('mathoholic.mathocheater.views',
    (r'^$', 'index'),
    (r'^(?P<d1>\d)(?P<d2>\d)(?P<d3>\d)(?P<d4>\d)$', 'solve')
)
