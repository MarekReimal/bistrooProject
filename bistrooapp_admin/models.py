from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    category_sort_id = models.PositiveIntegerField()

    class Meta: # on Country alam klass
        ordering = ["category_sort_id"]  # sorteerib tabeli
        verbose_name_plural = "categori_names" # et nätaks mitmuses

    def __str__(self): # et ei näitaks nimesid mitte objekt 1, objekt 2 jne
        return self.category_name # näitab ühte veergu loetava nimega

class Menuu(models.Model):
    menu_date = models.DateField()
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    price_full = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
    price_half = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:  # on Country alam klass
        ordering = ["-menu_date", "category_name", "description"]  # sorteerib tabeli

    def __str__(self):  # et ei näitaks nimesid mitte objekt 1, objekt 2 jne
        return f'{self.description}'  # näitab ühte veergu loetava nimega

class Theme(models.Model):
    menu_date = models.DateField(unique=True)
    theme = models.CharField(max_length=255, blank=True)
    recommenders = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255, blank=True)
    class Meta:
        ordering = ["-menu_date"] # sorteerib kahanevalt
        #unique_together = "menu_date" # https://www.letscodemore.com/blog/django-get-or-create/

    def __str__(self):
        return f'{self.theme}'

    def clean(self):
        if not self.theme or not self.recommenders:
            raise ValidationError("Üks kahest on puudu")
