from django.contrib import admin

from .models import Gamintojas, Modelis, Likutis, ModelisInstance

class ModelisAdmin(admin.ModelAdmin):
    list_display = ('modelis', 'gamintojas')

admin.site.register(Gamintojas)
admin.site.register(Modelis, ModelisAdmin)
admin.site.register(Likutis)
admin.site.register(ModelisInstance)