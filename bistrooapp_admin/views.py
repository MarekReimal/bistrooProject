from datetime import datetime, timedelta

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from bistrooapp_admin.models import Category, Menuu, Theme
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from .forms import (CurrentDate, ThemeForm, ThemeUpdateForm,
                    SublineUpdateForm, SublineForm, CategoryForm, DuplicateDate, MenuuSearchForm)


# Create your views here.

class CategoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "bistrooapp_admin/category.html"
    model = Category
    context_object_name = "categories"

    def test_func(self):
        return self.request.user.groups.filter(name='kasutajad').exists()


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = "bistrooapp_admin/category_create.html"
    model = Category
    #fields = "__all__"  # kõik väljad näha loomise vaatel
    success_url = reverse_lazy("bistrooapp_admin:category")
    form_class = CategoryForm

    def test_func(self):
        return self.request.user.groups.filter(name='kasutajad').exists()


class CategoryDeleteView(DeleteView):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)  # võtab modelist vastava kategooria obj
        category_name = category.category_name  # võtab mällu kateg. nime
        category.delete()  # kustutab elemendi
        # Set a success message
        messages.error(request, f"\"{category_name}\" kustutatud.")

        return HttpResponseRedirect(reverse("bistrooapp_admin:category"))


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "bistrooapp_admin/category_form_update.html"
    model = Category
    #fields = "__all__"
    success_url = reverse_lazy("bistrooapp_admin:category")
    form_class = CategoryForm

    def test_func(self):
        return self.request.user.groups.filter(name='kasutajad').exists()


def is_user(user):  # meetod teeb päringu db, kontroll kas kasutaja kuulub ligipääsu õigustega gruppi
    return user.groups.filter(name='kasutajad').exists()  # kui kasutaja kuulub gruppi kasutajad siis pääseb sisse logides


@user_passes_test(is_user)  # dekoraator kaitseb vaate sisselogimisega
def menuu_list(request):
    # tegeleb töölaua kuvamisega

    # Loob muutujad andmete saatmiseks html-le mõlemast mudelist
    categories = Category.objects.all()

    # töötleb menüü kuupäeva
    if request.method == "POST":
        # kui kaustaja valib kuupäeva, siis tehakse JS POST, korjab valitud kuupäeva
        if request.POST.get("valitud_kp"): # kui postis on kuupäev siis
            valitud_kp = request.POST.get("valitud_kp")  # on kujul 2023-12-06
            request.session['menu_date'] = valitud_kp
        else:  # kui kuupäeva ei ole siis on täna
            valitud_kp = datetime.today()  # on kujul 2023-12-21 23:36:50.338385
            request.session['menu_date'] = valitud_kp.strftime("%Y-%m-%d")  # kirjutab kuupäeva mällu kujul 2023-12-21

    elif request.session.get("menu_date"):  # kui kuupäev olemas mälus siis vali see
        valitud_kp = request.session.get('menu_date')
        # del request.session['menu_date']  # kustutab kuupäeva sessiooni mälust
    else:  # muul juhul on tänane kuupäev
        valitud_kp = datetime.today()
        request.session['menu_date'] = valitud_kp.strftime("%Y-%m-%d")  # kirjutab kuupäeva mällu

    # Set the expiry time for the 'menu_date' session variable to 1 hour
    request.session.set_expiry(timedelta(hours=2))

    #if request.session.get("menu_date"):
    # print("SESSIOONI KUUPÄEV ", request.session.get("menu_date"))  # testimiseks

    # teeb päringu DB, võtab menüü valitud kuupäeva järgi
    q_result_menuu = Menuu.objects.filter(menu_date=valitud_kp)
    q_result_theme = Theme.objects.filter(menu_date=valitud_kp)
    # print("Q_RESULT_MENUU ", q_result_menuu)  # testimiseks
    # print("Q_RESULT_THEME ", q_result_theme)  # testimiseks

    theme_id = None
    if q_result_theme.exists():  # võta pealkirja id, vajalik CRUD linkidele
        theme_id = q_result_theme.first().id

    # kuupäeva vormindamine vastavalt sellele kust pärineb
    # kontroll kas valitud_kp on string või datetime object
    if isinstance(valitud_kp, str):  # isinstance- kontrollib type ehk kas on str kui on POST siis on str type
        # kuupäeva vormindamine, vajalik teate väljastamiseks 18.11 Menüü puudub
        # Convert the string date to a datetime object
        kp_obj = datetime.strptime(valitud_kp, "%Y-%m-%d")
        # Format the date as desired (14.11.2023)
        formatted_date = kp_obj.strftime("%d.%m.%Y")
        default_date = kp_obj.strftime("%Y-%m-%d") #  "%Y-%m-%d"
    else:
        formatted_date = valitud_kp.strftime("%d.%m.%Y")
        default_date = valitud_kp.strftime("%Y-%m-%d") # "%Y-%m-%d"
        kp_obj = datetime.strptime(default_date, "%Y-%m-%d")

    # menüü vanuse kontroll
    # kas menüü kuupäev on minevikus või täna homme
    current_date_str = datetime.today().strftime("%Y-%m-%d")  # loob tänase kp str sobivas formaadis
    if kp_obj >= datetime.strptime(current_date_str, "%Y-%m-%d"):
        is_current = True
    else:
        is_current = False

    # loob obj form.py loodud kuupäeva vormile, vt form.py
    datePicker = CurrentDate(initial={"valitud_kp": default_date})  # määrab vaikimisi värtuse

    # loob vormi koopia kuupäeva jaoks
    if request.session.get('menu_date_duplicate'):  # kui sessi mälus on kuupäev siis
        dup_date = request.session.get('menu_date_duplicate')
        duplicate_date = DuplicateDate(initial={"duplikaadi_kp": dup_date})
    else:
        duplicate_date = DuplicateDate(initial={"duplikaadi_kp": datetime.today()})

    # Create a context dictionary with the data, andmed saadetakse html lehele
    context = {
        'categories': categories,
        'menuu_items': q_result_menuu,
        'themes': q_result_theme,
        'datePicker': datePicker, # form'i nimetus määratud, form loodud forms.py
        'formatted_date':  formatted_date,
        'theme_id': theme_id,
        "duplicate_date": duplicate_date,
        "is_current": is_current
    }
    return render(request, 'bistrooapp_admin/menuu_list.html', context)


@user_passes_test(is_user)  # dekoraator kaitseb vaate sisselogimisega
def add_subline(request, category):

    # võtab jooksva kuupäeva sessiooni mälust
    valitud_kp = request.session.get("menu_date")

    #  võtab modelist vastava kategooria obj, vajalik et oleks DB obj, cat sisaldab str ja see ei sobi
    categoryus = Category.objects.get(category_name=category)

    if request.method == "POST":
        subline_form = SublineForm(request.POST)
        if subline_form.is_valid():
            subline_form.save()
            return redirect("bistrooapp_admin:menuu_list")
    else:  # kuva vorm kui ei ole post, eelväärtusta kuupäev ja kategooria peidetud väljadel
        subline_form = SublineForm(initial={"menu_date": valitud_kp, "category_name": categoryus})

    current_date = datetime.strptime(valitud_kp, "%Y-%m-%d")  # vorminda obj, kp kuvamiseks templ.
    # väärtused kaasa templatele
    context = {
        "subline_form": subline_form,
        "categoryus": categoryus,
        "current_date": current_date
        }

    # mis on return render(request
# https://stackoverflow.com/questions/58563294/how-does-return-renderrequest-path-path-works-in-django
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Introduction
    return render(request, "bistrooapp_admin/menuu_add.html", context)


@user_passes_test(is_user)  # dekoraator kaitseb vaate sisselogimisega
def add_theme(request):
    # vaade pealkirjade sisestamiseks
    # vaade theme_create.html
    # on kaks juhtumit

    # võtab jooksva kuupäeva sessiooni mälust
    valitud_kp = request.session.get("menu_date")
    current_date = datetime.strptime(valitud_kp, "%Y-%m-%d")  # vorminda obj, kp kuvamiseks templ.

    # valik kas kuvada tühi vorm või täidetud vorm
    if not Theme.objects.filter(menu_date=valitud_kp).exists():  # kas kp obj on olemas
        # loob form obj ja annab kuupäeva väärtuse kaasa
        theme_formike = ThemeForm(initial={"menu_date": valitud_kp})
    else:  # Kui andme obj olemas siis kuvab täidetud andmetega
        theme_id = Theme.objects.get(menu_date=valitud_kp).id  # võta kp obj id
        # võtab modelist andmeobj, kui sellist andmeobj ei ole siis 404 teade
        theme_instance = get_object_or_404(Theme, id=theme_id)
        theme_formike = ThemeForm(instance=theme_instance)  # loob vormi obj eeltäidetud

    if request.method == "POST":
        menu_date = request.POST.get("menu_date")  # võta kp
        theme = request.POST.get("theme")
        recommenders = request.POST.get("recommenders")
        author = request.POST.get("author")

        if theme or recommenders or author:  # kui kasutaja sisestas vormile midagi siis toimetab, muidu jätab salvestamata
            # kasutaja tahab lisada ja andme obj selle kuupäevaga veel ei ole, siis sisestatakse uus rida
            if not Theme.objects.filter(menu_date=menu_date).exists():  # kui rida ei ole DB's
                theme_formike = ThemeForm(request.POST)
                if theme_formike.is_valid():
                    theme_formike.save()  # salvestab andmed POST'ist
                    return redirect("bistrooapp_admin:menuu_list")
            # kasutaja tahab lisada aga selle kuupäevaga rida on juba olemas
            # kui kp rida on, siis võtab obj id ja teeb andmete update
            else:  # kui rida on olemas DB's
                # võtab olemas oleva rea id
                theme_id = Theme.objects.get(menu_date=menu_date).id
                theme_instance = get_object_or_404(Theme, id=theme_id)  # võta id-le vastav obj
                theme_formike = ThemeForm(request.POST, instance=theme_instance)  # init form
                if theme_formike.is_valid():
                    # kui andmed ok siis kirjutab mällu
                    theme_formike.save()
                    return redirect("bistrooapp_admin:menuu_list")
        else:

            return redirect("bistrooapp_admin:menuu_list")

    return render(request, 'bistrooapp_admin/theme_add.html',
                  {"theme_formike": theme_formike, "current_date": current_date})


@user_passes_test(is_user)  # dekoraator kaitseb vaate sisselogimisega
def update_theme(request, theme_id):
    # 1. meetod võtab modelist obj ja kuvab vormi selle obj andmetega
    # 2. kui kasutaja sisestab vormi, siis POST ja vormilt andmed salvestatakse

    # võtab jooksva kuupäeva sessiooni mälust
    valitud_kp = request.session.get("menu_date")
    current_date = datetime.strptime(valitud_kp, "%Y-%m-%d")  # vorminda obj, kp kuvamiseks templ.

    # võtab modelist andmeobj, kui sellist andmeobj ei ole siis 404 teade
    theme_instance = get_object_or_404(Theme, id=theme_id)
    # kui andmeid sisestati siis
    if request.method == "POST":
        # loob vormi obj andmetega mis on POST ja seob uue obj olemasoleva obj-ga
        theme_up_form = ThemeUpdateForm(request.POST, instance=theme_instance)
        if theme_up_form.is_valid():
            # kui andmed ok siis kirjutab mällu
            theme_up_form.save()
            return redirect("bistrooapp_admin:menuu_list")
    else:
        theme_up_form = ThemeUpdateForm(instance=theme_instance)

    return render(request,"bistrooapp_admin/theme_update.html",
                  {"theme_up_form": theme_up_form, "theme_id": theme_id, "current_date": current_date})

def mytoday(request):

    #request.session['menu_date'] = None
    #print("SESSIOONI lahtesta KUUPÄEV ", request.session.get("menu_date"))  # testimiseks

    if 'menu_date' in request.session:
        del request.session['menu_date']  # kustutab kuupäeva sessiooni mälust
                                        # uus kp tekib menuu_list
    return redirect('bistrooapp_admin:menuu_list')


def move_back(request):
    if 'menu_date' in request.session:  # kui kp on olemas sess mälus
        menu_date = request.session.get("menu_date")  # võta kp
        kp_obj = datetime.strptime(menu_date, "%Y-%m-%d")  # vorminda obj
        kp_obj = kp_obj - timedelta(days=1)  # arvuta eilne kp
        menu_date = kp_obj.strftime("%Y-%m-%d")  # vorminda str
        request.session['menu_date'] = menu_date  # kirjuta sess mällu
    else:
        kp = datetime.today() - timedelta(days=1)  # arvuta eilne kp
        request.session['menu_date'] = kp.strftime("%Y-%m-%d")  # kirjutab kuupäeva mällu
    return redirect('bistrooapp_admin:menuu_list')


def move_forward(request):
    if 'menu_date' in request.session:  # kui kp on olemas sess mälus
        menu_date = request.session.get("menu_date")  # võta kp
        kp_obj = datetime.strptime(menu_date, "%Y-%m-%d")  # vorminda obj
        kp_obj = kp_obj + timedelta(days=1)  # arvuta homne kp
        menu_date = kp_obj.strftime("%Y-%m-%d")  # vorminda str
        request.session['menu_date'] = menu_date  # kirjuta sess mällu
    else:  # kui kp ei ole sess mälus
        kp = datetime.today() + timedelta(days=1)  # arvuta homne kp
        request.session['menu_date'] = kp.strftime("%Y-%m-%d")  # kirjutab kuupäeva mällu
    return redirect('bistrooapp_admin:menuu_list')


def delete_author(request, theme_id):
    theme_instance = Theme.objects.get(id=theme_id)  # võta vastava id-ga obj
    author = theme_instance.author
    if theme_instance.theme:  # kui teema on olemas siis kustutab ainult autori
        theme_instance.author = None
        theme_instance.save()
    elif theme_instance.theme is None:  # kui teemat ka ei ole siis kustutab terve obj
        theme_instance.delete()

    messages.success(request, author + " kustutatud")
    return redirect('bistrooapp_admin:menuu_list')


def delete_theme(request, theme_id):
    theme_instance = Theme.objects.get(id=theme_id)  # võta vastava id-ga obj
    theme = theme_instance.theme
    if theme_instance.author is None:  # kui autorit ka ei ole siis kustutab terve rea
        theme_instance.delete()
    elif theme_instance.author:  # kui autor on siis kustutab teema ja soovitajad
        theme_instance.theme = None
        theme_instance.recommenders = None
        theme_instance.save()
    messages.success(request, theme + " kustutatud")
    return redirect('bistrooapp_admin:menuu_list')


@user_passes_test(is_user)  # dekoraator kaitseb vaate sisselogimisega
def update_subline(request, line_id):
    # võtab jooksva kuupäeva sessiooni mälust
    valitud_kp = request.session.get("menu_date")
    current_date = datetime.strptime(valitud_kp, "%Y-%m-%d")  # vorminda obj

    # võtab modelist andmeobj, kui sellist andmeobj ei ole siis 404 teade
    line_instance = get_object_or_404(Menuu, id=line_id)
    # kui andmeid sisestati siis
    if request.method == "POST":
        # loob vormi obj andmetega mis on POST ja seob uue obj olemasoleva obj-ga
        subline_up_form = SublineUpdateForm(request.POST, instance=line_instance)
        if subline_up_form.is_valid():
            # kui andmed ok siis kirjutab mällu
            subline_up_form.save()
            return redirect("bistrooapp_admin:menuu_list")
    else:  # kui ei ole post siis kuva vorm
        subline_up_form = SublineUpdateForm(instance=line_instance)

    return render(request, "bistrooapp_admin/menuu_update.html",
                  {"subline_up_form": subline_up_form, "line_id": line_id, "current_date": current_date})

def delete_subline(request, line_id):
    # võtab modelist andmeobj, kui sellist andmeobj ei ole siis 404 teade
    line_instance = get_object_or_404(Menuu, id=line_id)
    description = line_instance.description
    line_instance.delete()
    messages.success(request, description + " kustutatud")
    #return redirect("bistrooapp_admin:menuu_list")
    return HttpResponseRedirect(reverse("bistrooapp_admin:menuu_list"))


def dublicate_message(request):
    # meetod näitab teadet, et tehakse koopia ja kirjutab vormilt saadud kuupäeva sessiooni mällu
    # võtab kasutaja antud kuupäeva
    if request.method == "POST":
        duplikaadi_kp = request.POST.get("duplikaadi_kp")  # on kujul 2023-12-06
        request.session['menu_date_duplicate'] = duplikaadi_kp  # kirjuta sess mällu
        duplikaadi_kp = datetime.strptime(duplikaadi_kp, "%Y-%m-%d")  # vorminda obj

    # võtab jooksva kuupäeva sessiooni mälust
    valitud_kp = request.session.get("menu_date")
    valitud_kp = datetime.strptime(valitud_kp, "%Y-%m-%d")  # vorminda obj

    return render(request, "bistrooapp_admin/duplicate_message.html",
                  {"duplikaadi_kp": duplikaadi_kp, "valitud_kp": valitud_kp})


def duplicate_menu(request):
    # meetod teeb menüüst koopia
    # võtab kasutaja antud kuupäeva
    #if request.method == "POST":
    #    duplikaadi_kp = request.POST.get("duplikaadi_kp")  # on kujul 2023-12-06
    #   request.session['menu_date_duplicate'] = duplikaadi_kp  # kirjuta sess mällu

    # võtab jooksva kuupäeva sessiooni mälust
    duplikaadi_kp = request.session.get("menu_date_duplicate")
    # võtab jooksva kuupäeva sessiooni mälust
    valitud_kp = request.session.get("menu_date")

    if not duplikaadi_kp == valitud_kp:  # teeb koopia ainult siis kui kuupäevad on
                                                                # erinevad (muidu kustutas kui olid samad kuupäevad)
        # teeb päringu DB, võtab menüü valitud kuupäeva järgi
        q_result_menuu = Menuu.objects.filter(menu_date=valitud_kp)
        q_result_theme = Theme.objects.filter(menu_date=valitud_kp)

        # kontroll kas sama kuupäevaga ridu on, et ei loodaks topelt
        q_result_menuu_dub = Menuu.objects.filter(menu_date=duplikaadi_kp)
        q_result_theme_dub = Theme.objects.filter(menu_date=duplikaadi_kp)
        if q_result_theme_dub:  # kontroll kas sama kuupäevaga ridu on, et ei loodaks topelt
            theme_instance_dub = Theme.objects.get(menu_date=duplikaadi_kp)  # võta vastava id-ga obj
            theme_instance_dub.delete()  # kustutab rea et ei teeks topelt
        if q_result_menuu_dub:  # kui on ridu siis kustutab
            for obj in q_result_menuu_dub:  # loendab kõik read õige kuupäevaga
                obj.delete()  # kustutab rea

        # kui menüül on teemad siis teeb koopia uue kuupäevaga
        if q_result_theme:
            # võtab väärtused olemas olevast menüüst
            theme_instance = Theme.objects.get(menu_date=valitud_kp)  # võta vastava id-ga obj
            new_theme_instance = Theme.objects.create(
                menu_date=duplikaadi_kp,
                theme=theme_instance.theme,
                recommenders=theme_instance.recommenders,
                author=theme_instance.author
            )
            new_theme_instance.save()

        # kui menüül on toidud siis teeb koopia uue kuupäevaga
        if q_result_menuu:
            for menu_instance in q_result_menuu:
                new_menu_instance = Menuu.objects.create(
                    menu_date=duplikaadi_kp,
                    category_name=menu_instance.category_name,
                    description=menu_instance.description,
                    price_full=menu_instance.price_full,
                    price_half=menu_instance.price_half
                )
                new_menu_instance.save()

    return HttpResponseRedirect(reverse("bistrooapp_admin:menuu_list"))


@user_passes_test(is_user)  # dekoraator kaitseb vaate sisselogimisega
def menuu_search(request):  # vaade menüüdest otsimse vormile
    menuu_search_form = MenuuSearchForm()
    return render(request, "bistrooapp_admin/menuu_search.html",
                  {"menuu_search_form": menuu_search_form})


@user_passes_test(is_user)  # dekoraator kaitseb vaate sisselogimisega
def menuu_search_list(request):  # vaade kuvab otsingu tulemused menüüdest

    # kui andmeid sisestati siis
    if request.method == "POST":
        menuu_search_form = MenuuSearchForm(request.POST)
        if menuu_search_form.is_valid():
            search_phrase = menuu_search_form.cleaned_data["search_phrase"]
            request.session['search_phrase'] = search_phrase
            search_result_menuu = Menuu.objects.filter(description__contains=search_phrase)  # filtreerib otsingu järgi

        else:
            return render(request, "bistrooapp_admin/menuu_search.html",
                          {"menuu_search_form": menuu_search_form})

    else:  # kui ei ole post
        search_phrase = request.session.get('search_phrase')  # võta mälust viimane otsingu fraas
        search_result_menuu = Menuu.objects.filter(description__contains=search_phrase)  # filtreeri

    list_count = search_result_menuu.count()  # loendab mitu kirjet leiti

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(search_result_menuu, 10)  # Show 10 results per page
    try:
        search_result_menuu = paginator.page(page)
    except PageNotAnInteger:
        search_result_menuu = paginator.page(1)
    except EmptyPage:
        search_result_menuu = paginator.page(paginator.num_pages)

    return render(request, "bistrooapp_admin/menuu_search_list.html",
                      {"search_result_menuu": search_result_menuu, "list_count": list_count, "search_phrase":search_phrase})

def hide_row(request):
    # metod kirjutab modelisse rea peida/näita
    checkboxId = request.GET.get('checkboxId', None)  # võta rea id
    # võtab modelist andmeobj, kui sellist andmeobj ei ole siis 404 teade
    line_instance = get_object_or_404(Menuu, id=checkboxId)
    # kontroll mis väärtus on modelis
    if line_instance.is_hided:  # kui on True siis muudab Falseks
        line_instance.is_hided = False
    else:  # kui on False siis muudab Trueks
        line_instance.is_hided = True
    line_instance.save()  # salvestab väärtuse

    return HttpResponse()


def logout_view(request):
    # meetod logib välja kasutaja. Template'el on viide js. js laetakse browserisse ja aja arvestus toimub seal
    logout(request)
    # loob teate mida kuvatakse sisselogimise lehel
    messages.add_message(request, messages.WARNING, 'Oled välja logitud, jätkamiseks palun logi sisse')
    # return render(request, 'bistrooapp_admin/logout.html')
    return redirect("login")

def changeMenuuDate(request, line_id):
    # meetod muudab sessiooni mälus hoitava menüü kuupäeva ja suunab töölaua vaatele kus kuvatakse see menüü

    # võtab modelist andmeobj, kui sellist andmeobj ei ole siis 404 teade
    line_instance = get_object_or_404(Menuu, id=line_id)
    kp_obj = line_instance.menu_date  # võta kuupäev
    menu_date = kp_obj.strftime("%Y-%m-%d")  # vorminda str
    request.session['menu_date'] = menu_date  # kirjuta sess mällu
    return redirect("bistrooapp_admin:menuu_list")

"""

def add_subline_ei_kasuta(request, category): # algne töö, form oli tehtud html mitte django form
    # töötleb menuu_create.html
    # vaade toidu sisestamiseks
    valitud_kp = request.session.get('menu_date')

    # funkts parameetri category kaudu võetakse vastu category väärtus, saadetakse formile key categoryus, vt menuu_create.html
    return render(request, 'bistrooapp_admin/menuu_create.html', {'categoryus': category, 'valitud_kpius': valitud_kp})

def save_subline(request):
    # tegeleb vormilt toitude salvestamisega mudelisse
    # see funkts salvestab ainult formilt saadud andmed ja suunab tagasi vaatele menuu_list
    # ehk siis see on abi funktsioon andmete salvestamiseks

    if request.method == 'POST':
        menu_date = request.session.get('menu_date')  #request.POST.get("menu_date")
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
        if not price_half:
            price_half = None
        # Save the data to the Menuu model
        menuu = Menuu(menu_date=menu_date, category_name=category, description=description, price_full=price_full,
                      price_half=price_half)
        menuu.save()

        # salvestab vormiga saadetud kp sessiooni mällu, nii saab seda kuupäeva kasutada menuu_list
        request.session['menu_date']=menu_date

    return redirect('bistrooapp_admin:menuu_list')


def add_theme_ei_kasuta(request):
    # vaade pealkirjade sisestamiseks
    # vaade theme_create.html
    valitud_kp = request.session.get("menu_date")
    return render(request, 'bistrooapp_admin/theme_create.html', {'valitud_kpius': valitud_kp})


def save_theme_ei_kasuta(request):
    # tegeleb vormilt toitude salvestamisega mudelisse
    # see funkts salvestab ainult formilt saadud andmed ja suunab tagasi vaatele menuu_list
    # ehk siis see on abi funktsioon andmete salvestamiseks
    # hea lahendus- võimaldab andmed üle kirjutada ja hoiab kuupäeva unikaalsena selliselt

    if request.method == "POST":
        menu_date = request.POST.get("menu_date")
        theme = request.POST.get("theme")
        recommenders = request.POST.get("recommenders")
        author = request.POST.get("author")

        # vormindab suured tähed enne salvestamist
        theme = theme.upper()
        recommenders = recommenders.upper()
        author = author.upper()

    # andmete DB kirjutamine
    theme_instance, created = Theme.objects.get_or_create(
        # kontrollib kas kuupäev on tabelis
        menu_date=menu_date,
        # kui kuupäev ei ole tabelis siis kirjutab andmed DB
        defaults={"theme": theme, "recommenders": recommenders, "author": author})
    # kontroll, kui created=False siis kirjutab andmed üle. created=False on siis kui andmed olid olemas ja uut ei lisatud
    if not created:
        theme_instance.theme = theme
        theme_instance.recommenders = recommenders
        theme_instance.author = author
        theme_instance.save()


    
    ChatGPT
    The get_or_create method in Django returns a tuple of two values: the object retrieved or
     created (theme_instance in this case) and a boolean value (created) indicating whether the
      object was created (True) or retrieved from the database (False).

    theme_instance: This variable holds the retrieved or newly created object from the database. 
    If an object with the specified parameters (in this case, menu_date) already exists, 
    theme_instance will contain that object. If not, it will hold the newly created object.

    created: This boolean variable indicates whether the object was newly created (True) or already 
    existed in the database (False). It helps differentiate between the creation and retrieval of the object 
    based on the provided parameters.
    
    return redirect("bistrooapp_admin:menuu_list")
    
    """
