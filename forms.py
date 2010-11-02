from django import forms

class DigitsForm(forms.Form):
    digits = forms.IntegerField(min_value=0,max_value=9999)
