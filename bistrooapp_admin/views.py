from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from bistrooapp_admin.models import Category, Menuu
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.shortcuts import redirect


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

class MenuuListView(TemplateView):
    template_name = "bistrooapp_admin/menuu_list.html"
    model = Menuu

class MenuuCreateView(TemplateView):
    template_name = "bistrooapp_admin/menuu_create.html"
    model = Menuu
    #fields = "__all__"
    success_url = reverse_lazy("bistrooapp_admin:menuu_list")

def add_subline(request, category):
    return render(request, 'bistrooapp_admin/menuu_create.html', {'category': category})

def save_subline(request):
    if request.method == 'POST':
        menu_date = request.POST.get("menu_date")
        category_name = request.POST.get('category')
        print("MINU RIDA ", category_name)
        description = request.POST.get('description')
        price_full = request.POST.get('price_full')
        price_half = request.POST.get('price_half')
        # Initialize category with None (no category)
        category = None
        try:
            category = Category.objects.get(category_name=category_name)
        except Category.DoesNotExist:
           print("KATEGOORIAT EI OLE ")

        # Save the data to the Menuu model
        menuu = Menuu(menu_date=menu_date, category_name=category, description=description, price_full=price_full, price_half=price_half)
        menuu.save()

    return redirect('bistrooapp_admin:menuu_list')



    #def add_subline(request):
     #   category = request.GET.get('category', '')
      #  print("minu pudi " + category )
        # You can also handle the case when the category is not provided
       # return render(request, 'bistrooapp_admin/menuu_create.html', {'category': category})