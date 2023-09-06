from django.contrib import admin

from .models import Gamintojas, Modelis, Likutis, ModelisInstance

class ModeliaiInstanceInline(admin.TabularInline):
    model = ModelisInstance
    extra = 0

@admin.register(Modelis)
class ModelisAdmin(admin.ModelAdmin):
    list_display = ('modelis', 'gamintojas', 'display_likutis')
    inlines = [ModeliaiInstanceInline]

@admin.register(ModelisInstance)
class LikutisInstanceAdmin(admin.ModelAdmin):
    list_display = ('modelis', 'id', 'status', 'planuojama_gauti')
    list_filter = ('status', 'planuojama_gauti')

    fieldsets = (
        ('General', {'fields': ('id', 'modelis')}),
        ('Aavailability', {'fields': ('status', 'planuojama_gauti')}),
    )

@admin.register(Gamintojas)
class GamintojasAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'gaminimo_pradzia', 'display_modeliai')


#admin.site.register(Gamintojas)
#admin.site.register(Modelis, ModelisAdmin)
admin.site.register(Likutis)
#admin.site.register(ModelisInstance, LikutisInstanceAdmin)