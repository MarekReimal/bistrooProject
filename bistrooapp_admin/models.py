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