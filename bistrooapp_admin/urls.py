# minu tehtud fail
# juhend https://medium.com/@aman_adastra/day-8-of-100-days-of-django-multiple-applications-inside-django-project-3bf580760745
from django.urls import path
from . import views

app_name = "bistrooapp_admin"

urlpatterns = [
    path("", views.menuu_list, name="menuu_list"),  # kategooriad
    path("category/", views.CategoryListView.as_view(), name="category"),
    path("category_create/", views.CategoryCreateView.as_view(), name="category_create"),
    path("category_delete/<int:pk>", views.CategoryDeleteView.as_view(), name="category_delete"),
    path("category_update/<int:pk>", views.CategoryUpdateView.as_view(), name="category_update"),
    path("menuu_list/", views.menuu_list, name="menuu_list"),
    #path("menuu_create/", views.MenuuCreateView.as_view(), name="menuu_create"),

    #path('menu_categories/', views.menu_categories, name='menu_categories'),
    path("add_subline/<str:category>/", views.add_subline, name="add_subline"),
    #path("save_subline/", views.save_subline, name="save_subline"),
    path("add_theme/", views.add_theme, name="add_theme"),
    path("update_theme/<int:theme_id>", views.update_theme, name="update_theme"),
    path("delete_theme/<int:theme_id>", views.delete_theme, name="delete_theme"),
    path("delete_author/<int:theme_id>", views.delete_author, name="delete_author"),
    path("update_subline/<int:line_id>", views.update_subline, name="update_subline"),
    path("delete_subline/<int:line_id>", views.delete_subline, name="delete_subline"),

    path("today/", views.mytoday, name="today"), # kustutab sessioonist kp
    path("move_back/", views.move_back, name="move_back"),
    path("move_forward/", views.move_forward, name="move_forward"),

    path("duplicate_menu", views.duplicate_menu, name="duplicate_menu"),

    path("menuu_search/", views.menuu_search, name="menuu_search"),
    path("menuu_search_list/", views.menuu_search_list, name="menuu_search_list")
]