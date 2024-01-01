from datetime import datetime

from django.shortcuts import render

from bistrooapp_admin.models import Menuu, Theme


# Create your views here.

def show_menu(request):
    menu_date = datetime.today()
    # teeb päringu DB, võtab menüü valitud kuupäeva järgi
    q_result_menuu = Menuu.objects.filter(menu_date=menu_date).values("category_name__category_name",
                                                                      "description", "price_full", "price_half")
    q_result_theme = Theme.objects.filter(menu_date=menu_date)
    formatted_date = menu_date.strftime("%d.%m")  # väärtus template jaoks

    # Hinna töötlus, kirjutab "Prae hinna sees"
    for item in q_result_menuu:
        # Kui hind on 0 või 0 ja none
        if ((str(item["price_full"]) == "0.00" and str(item["price_half"]) == "0.00") or
                (str(item["price_full"]) == "0.00" and str(item["price_half"]) == "None")):
            # siis väärtus ...
            item["price_full"] = "Prae hinna sees"

        if str(item["price_half"]) == "0.00" or str(item["price_half"]) == "None":
            item["price_half"] = ""

    context = {
        "formatted_date": formatted_date,
        'menuu_items': q_result_menuu,
        'themes': q_result_theme,
    }
    return render(request, 'bistrooapp_public/index.html', context)
