from datetime import datetime

from django import forms

# https://mrasimzahid.medium.com/how-to-implement-django-datepicker-calender-in-forms-date-field-9e23479b5db

class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%d.%m.%Y'  # Define the desired date format


class CurrentDate(forms.Form):
    valitud_kp = forms.DateField(widget=DateInput, input_formats=['%d.%m.%Y'], label="Menüü kuupäev")  # , initial=datetime.now()

'''
    def clean_valitud_kp(self):
        date_kontrollitud = self.cleaned_data['valitud_kp']
        if not date_kontrollitud:
            return datetime.now()
        elif date_kontrollitud == datetime.now():
            return datetime.now()
        else:
            return date_kontrollitud
'''