from datetime import datetime

from django.shortcuts import render

from bistrooapp_admin.models import Menuu, Theme


# Create your views here.

def show_menu(request):
    menu_date = datetime.today()
    # teeb päringu DB, võtab menüü valitud kuupäeva järgi
    q_result_menuu = Menuu.objects.filter(menu_date=menu_date)
    q_result_theme = Theme.objects.filter(menu_date=menu_date)

    context = {
        'menuu_items': q_result_menuu,
        'themes': q_result_theme,
    }
    return render(request, 'bistrooapp_public/index.html', context)
