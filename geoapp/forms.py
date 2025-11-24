from django import forms

CONTINENT_CHOICES = [
    ('Africa', 'Africa'),
    ('Asia', 'Asia'),
    ('Europe', 'Europe'),
    ('Americas', 'Americas'),
    ('Oceania', 'Oceania'),
]

class ContinentForm(forms.Form):
    continent = forms.ChoiceField(choices=CONTINENT_CHOICES)

