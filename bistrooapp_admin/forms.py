from datetime import datetime

from django import forms
from .models import Theme, Menuu
from django.core.exceptions import ValidationError


# https://mrasimzahid.medium.com/how-to-implement-django-datepicker-calender-in-forms-date-field-9e23479b5db

class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%d.%m.%Y'  # Define the desired date format


class CurrentDate(forms.Form):
    valitud_kp = forms.DateField(widget=DateInput, input_formats=['%d.%m.%Y'], label="")
                                  # label="Menüü kuupäev" , initial=datetime.now()


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ["menu_date", "theme", "recommenders", "author"]
        widgets = {
            'menu_date': forms.HiddenInput(),  # Hide the menu_date field
        }

    """
    vormi kontroll, teeb sama töö mis models.py class Theme(models.Model): def clean
    töötav näidis
    
    def clean(self):
        cleaned_data = super().clean()
        theme = cleaned_data.get("theme")
        recom = cleaned_data.get("recommenders")
        print("VORMILT TEEMA",theme)  # test
        if not theme or not recom:
            print("VORMILT TEEMA", theme, "teeb if")  # test
            raise ValidationError("mingi jama on")
        return cleaned_data
    """

class ThemeUpdateForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ["theme", "recommenders", "author"]

class SublineUpdateForm(forms.ModelForm):
    class Meta:
        model = Menuu
        fields = ["description", "price_full", "price_half"]