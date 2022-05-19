from django.contrib import admin
from inventory_bd.models import Thing, Responsible


class ThingAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'inv', 'price', 'count', 'summ', 'note']


admin.site.register(Thing, ThingAdmin)


class ResponsibleAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Responsible, ResponsibleAdmin)



