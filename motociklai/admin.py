from django.contrib import admin

from .models import Gamintojas, Modelis, Likutis, ModelisInstance, ModelisReview

class ModeliaiInstanceInline(admin.TabularInline):
    model = ModelisInstance
    extra = 0

@admin.register(Modelis)
class ModelisAdmin(admin.ModelAdmin):
    list_display = ('modelis', 'gamintojas', 'display_likutis')
    search_fields = ('modelis', 'gamintojas__pavadinimas')
    inlines = [ModeliaiInstanceInline]



@admin.register(ModelisInstance)
class LikutisInstanceAdmin(admin.ModelAdmin):
    list_display = ('modelis', 'id', 'status', 'planuojama_gauti', 'klientas')
    list_editable = ('status', 'planuojama_gauti',  'klientas',)
    list_filter = ('status', 'planuojama_gauti')
    search_fields = ('id', 'modelis__modelis')

    fieldsets = (
        ('General', {'fields': ('id', 'modelis')}),
        ('Aavailability', {'fields': ('status', 'planuojama_gauti','klientas',)}),
    )

@admin.register(Gamintojas)
class GamintojasAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'gaminimo_pradzia', 'display_modeliai')

@admin.register(ModelisReview)
class ModelisReviewAdmin(admin.ModelAdmin):
    list_display = ('modelis', 'date_created', 'reviewer', 'content')




#admin.site.register(Gamintojas)
#admin.site.register(Modelis, ModelisAdmin)
admin.site.register(Likutis)
#admin.site.register(ModelisInstance, LikutisInstanceAdmin)