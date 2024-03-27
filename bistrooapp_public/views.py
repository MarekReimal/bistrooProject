from datetime import datetime

from django.shortcuts import render

from bistrooapp_admin.models import Menuu, Theme


# Create your views here.

def show_menu(request):
    menu_date = datetime.today()
    # teeb päringu DB, võtab menüü valitud kuupäeva järgi
    q_result_menuu = (Menuu.objects.filter(menu_date=menu_date).
                      values("category_name__category_name", "description", "price_full", "price_half", "is_hided"))
    q_result_theme = Theme.objects.filter(menu_date=menu_date)
    formatted_date = menu_date.strftime("%d.%m.%Y")  # väärtus template jaoks

    # kontroll kas tänase menüü andmed on, kasutab public vaatel teate näitamiseks
    if q_result_menuu or q_result_theme:
        is_menuu = True
    else:
        is_menuu = False

    # Hinna töötlus, kirjutab "Prae hinna sees"
    for item in q_result_menuu:
        # print(item["price_full"])
        # if item["price_full"] == 0:
        #     print("OLI NULL")
        # Kui täis ja pool hind on olemas siis näitab mõlemat
        if str(item["price_full"]) > "0.00" and (str(item["price_half"]) > "0.00" and str(item["price_half"]) != "None"):
            item["price_full"] = str(item["price_full"]) + " / " + str(item["price_half"])
        # Kui täishind on 0 ja poolhind 0 või none siis näitab prae hinna sees
        elif ((str(item["price_full"]) == "0.00" and str(item["price_half"]) == "0.00") or
                (str(item["price_full"]) == "0.00" and str(item["price_half"]) == "None")):
            item["price_full"] = "Prae hinna sees"

    context = {
        "formatted_date": formatted_date,
        "is_menuu": is_menuu,
        "menuu_items": q_result_menuu,
        "themes": q_result_theme,
    }
    return render(request, "bistrooapp_public/index.html", context)
