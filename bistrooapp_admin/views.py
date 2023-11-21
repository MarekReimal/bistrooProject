from datetime import datetime

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from bistrooapp_admin.models import Category, Menuu
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from .forms import CurrentDate


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


class CategoryDeleteView(DeleteView):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()

        # Set a success message
        messages.error(request, f"Kustutati kategooria \"{category.category_name}\".")

        return HttpResponseRedirect(reverse("bistrooapp_admin:category"))


class CategoryUpdateView(UpdateView):
    template_name = "bistrooapp_admin/category_form_update.html"
    model = Category
    fields = "__all__"
    success_url = reverse_lazy("bistrooapp_admin:category")


#class MenuuListView(ListView):
 #   template_name = "bistrooapp_admin/menuu_list.html"
  #  model = Menuu

   # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
     #   context['categories'] = Category.objects.all()  # Retrieve all Category instances
      #  return context


def menuu_list(request):
    # Loob muutujad andmete saatmiseks html-le mõlemast mudelist
    categories = Category.objects.all()
    menuu_items = Menuu.objects.all()

    if request.session.get('menu_date'):
        valitud_kp = request.session.get('menu_date')
        del request.session['menu_date']  # kustutab kuupäeva sessiooni mälust
    elif request.method == "POST":
        # kui kaustaja valib kuupäeva, siis tehakse JS POST, korjab valitud kuupäeva
        valitud_kp = request.POST.get("valitud_kp")
        #print("MINU KUUPÄEV ", valitud_kp)  # testimiseks
    else:
        valitud_kp = datetime.today()

    # teeb päringu DB, võtab menüü valitud kuupäeva järgi
    q_result = Menuu.objects.filter(menu_date=valitud_kp)
    # print("Q_RESULT ", q_result)  # testimiseks

    if isinstance(valitud_kp, str):  # kui on POST siis on str type
        # kuupäeva vormindamine, vajalik teate väljastamiseks 18.11 Menüü puudub
        # Convert the string date to a datetime object
        kp_obj = datetime.strptime(valitud_kp, "%Y-%m-%d")
        # Format the date as desired (14.11.2023)
        formatted_date = kp_obj.strftime("%d.%m")
        default_date = kp_obj.strftime("%Y-%m-%d")
    else:
        formatted_date = valitud_kp.strftime("%d.%m")
        default_date = valitud_kp.strftime("%Y-%m-%d")

    # loob obj form.py loodud kuupäeva vormile, vt form.py
    datePicker = CurrentDate(initial={"valitud_kp": default_date})  # määrab vaikimisi värtuse

    # Create a context dictionary with the data, andmed saadetakse html lehele
    context = {
        'categories': categories,
        'menuu_items': q_result,
        'formike': datePicker, # form'i nimetus määratud, form loodud forms.py
        'formatted_date':  formatted_date
    }

    return render(request, 'bistrooapp_admin/menuu_list.html', context)


def add_subline(request, category):
    # funkts parameetri category kaudu võetakse vastu category väärtus, saadetakse formile key categoryus, vt menuu_create.html
    return render(request, 'bistrooapp_admin/menuu_create.html', {'categoryus': category})


def save_subline(request):
    if request.method == 'POST':
        menu_date = request.POST.get("menu_date")
        cat = request.POST.get('category_name')
        description = request.POST.get('description')
        price_full = request.POST.get('price_full')
        price_half = request.POST.get('price_half')

        #print("MINU KUUPÄEV ", menu_date)  # testimiseks
        #print("MINU KATEGOORIA ", cat)
        #print("MINU KIRJELDUS ", description)
        #print("MINU HIND TÄIS ", price_full)
        #print("MINU HIND POOL ", price_half)

        #  võtab modelist vastava kategooria obj, vajalik et oleks DB obj, cat sisaldab str ja see ei sobi
        category = Category.objects.get(category_name=cat)

        # Save the data to the Menuu model
        menuu = Menuu(menu_date=menu_date, category_name=category, description=description, price_full=price_full, price_half=price_half)
        menuu.save()

        # salvestab vormiga saadetud kp sessiooni mällu, nii saab seda kuupäeva kasutada menuu_list
        request.session['menu_date']=menu_date

    return redirect('bistrooapp_admin:menuu_list')