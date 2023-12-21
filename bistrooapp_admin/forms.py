from datetime import datetime

from django import forms
from .models import Theme, Menuu, Category
from django.core.exceptions import ValidationError


# https://mrasimzahid.medium.com/how-to-implement-django-datepicker-calender-in-forms-date-field-9e23479b5db

class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%d.%m.%Y'  # Define the desired date format


class CurrentDate(forms.Form):
    valitud_kp = forms.DateField(widget=DateInput(attrs={"class": "datepicker-form"}), input_formats=['%d.%m.%Y'], label="")
                                  # label="Menüü kuupäev" , initial=datetime.now()


class DublicateDate(forms.Form):
    dublikaadi_kp = forms.DateField(widget=DateInput(attrs={"class": "datepicker-form"}), input_formats=['%d.%m.%Y'])


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name", "category_sort_id"]
        labels = {"category_name": "Toidu kategooria", "category_sort_id": "Järjestus nr"}
        error_messages = {"category_name":{"required": "Väli on nõutud"},
                          "category_sort_id":{"required": "Väli on nõutud", "min_value": "Väärtus peab olema 0 või 0-st suurem number"}}





class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ["menu_date", "theme", "recommenders", "author"]
        labels = {"theme": "Teema", "recommenders": "Soovitajad", "author": "Autor"}
        widgets = {
            "menu_date": forms.HiddenInput()  # Hide the menu_date field
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
        labels = {"theme": "Teema", "recommenders": "Soovitajad", "author": "Autor"}



class SublineForm(forms.ModelForm):
    class Meta:
        model = Menuu
        fields = ["menu_date", "category_name", "description", "price_full", "price_half"]
        labels = {"description": "Nimetus", "price_full": "Hind suurele", "price_half": "Hind väiksele"}
        widgets = {"menu_date": forms.HiddenInput, "category_name": forms.HiddenInput}
        error_messages = {"description": {"required": "Väli on nõutud"},
                          "price_full": {"required": "Väli on nõutud, 0 või 0-st suurem number"}}
# https://stackoverflow.com/questions/3436712/create-custom-error-messages-with-model-forms

class SublineUpdateForm(forms.ModelForm):
    class Meta:
        model = Menuu
        fields = ["description", "price_full", "price_half"]
        labels = {"description": "Nimetus", "price_full": "Hind suurele", "price_half": "Hind väiksele"}
        error_messages = {"description": {"required": "Väli on nõutud"},
                          "price_full": {"required": "Väli on nõutud, 0 või 0-st suurem number"}}
