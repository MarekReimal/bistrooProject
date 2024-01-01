# minu tehtud fail
# juhend https://medium.com/@aman_adastra/day-8-of-100-days-of-django-multiple-applications-inside-django-project-3bf580760745

from django.urls import path
from . import views

app_name = "bistrooapp_public"


urlpatterns = [
    path("", views.show_menu, name="index"),  # avaleht
]