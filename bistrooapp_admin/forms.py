from datetime import datetime

from django import forms
from .models import Theme

# https://mrasimzahid.medium.com/how-to-implement-django-datepicker-calender-in-forms-date-field-9e23479b5db

class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%d.%m.%Y'  # Define the desired date format


class CurrentDate(forms.Form):
    valitud_kp = forms.DateField(widget=DateInput, input_formats=['%d.%m.%Y'], label="Menüü kuupäev")  # , initial=datetime.now()

class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ["menu_date", "theme", "recommenders", "author"]