from django import forms

class DigitsForm(forms.Form):
    """Optimally, this will be a field that requires 4 digits;
     0019 will work.  0+0+1+9 = 10 but 19 is actually invalid for the game."""
    digits = forms.IntegerField(min_value=19,max_value=9999)
