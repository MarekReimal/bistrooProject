# minu tehtud fail
# juhend https://medium.com/@aman_adastra/day-8-of-100-days-of-django-multiple-applications-inside-django-project-3bf580760745
from django.urls import path
from . import views

app_name = "bistrooapp_admin"

urlpatterns = [
    path("", views.CategoryHomeView.as_view(), name="index"),  # kategooriad
    path("category/", views.CategoryListView.as_view(), name="category"),
    path("category_create/", views.CategoryCreateView.as_view(), name="category_create"),
    path("category_delete/<int:pk>", views.CategoryDeleteView.as_view(), name="category_delete"),
    path("category_update/<int:pk>", views.CategoryUpdateView.as_view(), name="category_update"),
    path("menuu_list/", views.menuu_list, name="menuu_list"),
    #path("menuu_create/", views.MenuuCreateView.as_view(), name="menuu_create"),

    #path('menu_categories/', views.menu_categories, name='menu_categories'),
    path('add_subline/<str:category>/', views.add_subline, name='add_subline'),
    path('save_subline/', views.save_subline, name='save_subline'),
    path('add_theme/', views.add_theme, name='add_theme'),
    #path('save_theme/', views.save_theme, name='save_theme'),

    path('lahtesta/', views.lahtesta, name='lahtesta'), # kustutab sessioonist kp
]