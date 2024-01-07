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
        # Kui täis ja pool hind on olemas siis näitab mõlemat
        if str(item["price_full"]) > "0.00" and (str(item["price_half"]) > "0.00" and str(item["price_half"]) != "None"):
            item["price_full"] = str(item["price_full"]) + " / " + str(item["price_half"])
        # Kui täishind on 0 ja poolhind 0 ja none siis näitab prae hinna sees
        elif ((str(item["price_full"]) == "0.00" and str(item["price_half"]) == "0.00") or
                (str(item["price_full"]) == "0.00" and str(item["price_half"]) == "None")):
            item["price_full"] = "Prae hinna sees"


    context = {
        "formatted_date": formatted_date,
        'menuu_items': q_result_menuu,
        'themes': q_result_theme,
    }
    return render(request, 'bistrooapp_public/index.html', context)
