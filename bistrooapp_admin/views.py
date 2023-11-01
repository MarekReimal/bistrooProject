from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView

from bistrooapp_admin.models import Category
from django.urls import reverse_lazy

# Create your views here.

class CategoryHomeView(TemplateView): # näitab ava lehte
    template_name = "bistrooapp_admin/index.html" # movieapp/templates/index.html

class CategoryListView(ListView):
    template_name = "bistrooapp_admin/category.html"
    model = Category
    context_object_name = "categories"

class CategoryCreateView(CreateView):
    template_name = "bistrooapp_admin/category_create.html"
    model = Category
    fields = "__all__"  # kõik väljad näha loomise vaatel
    success_url = reverse_lazy("bistrooapp_admin:category")