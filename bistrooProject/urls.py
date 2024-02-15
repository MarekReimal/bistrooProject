"""
URL configuration for bistrooProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include    # include minu lisatud
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("bistrooapp_admin/", include("bistrooapp_admin.urls")),  # rida ütleb et movieapp lingid on failis "movieapp.urls"
    path("bistrooapp_public/", include("bistrooapp_public.urls")),  # rida ütleb et movieapp lingid on failis "movieapp.urls"
    path("", RedirectView.as_view(url="bistrooapp_public")),  # suunab faili kus on lingid booksapp.urls.py
                                                    # kui on http://127.0.0.1:8000 siis see rida
                                                    # lisab "movieapp" ehk http://127.0.0.1:8000/movieapp/
                                        # kui vaatad api urls.py, seal on avaleht "", mis tähendab et kui on
                                # http://127.0.0.1:8000/movieapp/"siin on tühi", siis teab et vaja avada avaleht
    # siin redirect suunab bistrooapp_public index.html
    # kui tahad bistrooapp_admin index.html siis vaja käsitsi kirjutada url http://127.0.0.1:8000/bistrooapp_admin/


    #path("accounts/", include("django.contrib.auth.urls")),  # link sisselogimise lehele
    path("accounts/", include("django.contrib.auth.urls")),  # link sisselogimise lehele
]
