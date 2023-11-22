from django.contrib import admin
from . models import * # kõik mudelid saavad siia faili

# Register your models here.

admin.site.register(Category) # näita Country model
admin.site.register(Menuu) # näita Language model
admin.site.register(Theme)