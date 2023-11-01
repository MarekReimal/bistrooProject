from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class HomeView(TemplateView): # näitab ava lehte
    template_name = "bistrooapp_public/index.html" # movieapp/templates/index.html
