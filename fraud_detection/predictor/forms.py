import json
from django import forms
from django.conf import settings

# Load choices from JSON file
with open(r'C:\Users\abdes\Desktop\MIAAD\S3\DL\Fraud_detaction\fraud_detection\predictor\JSON\choices.json') as f:
    choices = json.load(f)

class TransactionForm(forms.Form):
    amt = forms.FloatField(label='Transaction Amount', widget=forms.NumberInput(attrs={'placeholder': 'Enter Amount'}))
    gender = forms.ChoiceField(choices=[(g, g) for g in choices['gender']], label='Gender')
    age = forms.IntegerField(label='Age', widget=forms.NumberInput(attrs={'placeholder': 'Enter Age'}))

    category = forms.ChoiceField(choices=[(c, c) for c in choices['category']], label='Category')
    # merchant = forms.ChoiceField(choices=[(m, m) for m in choices['merchant']], label='Merchant')
    city = forms.ChoiceField(choices=[(c, c) for c in choices['city']], label='City')
    # city_pop = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    # state = forms.ChoiceField(choices=[(s, s) for s in choices['state']], label='State')
    # street = forms.ChoiceField(choices=[(s, s) for s in choices['street']], label='Street')
    # zip = forms.ChoiceField(choices=[(z, z) for z in choices['zip']], label='ZIP Code')
    # job = forms.ChoiceField(choices=[(j, j) for j in choices['job']], label='Job')

    unix_time = forms.DateTimeField(label='Transaction Date and Time', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
