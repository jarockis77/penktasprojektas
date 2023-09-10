from django.urls import path

from . import views

urlpatterns = [
    path('', views.index,  name='index-url'),
    path('gamintojai/', views.gamintojai, name='gamintojai-visi-url'),
    path('gamintojai/<int:gamintojas_id>', views.gamintojas, name='gamintojas-vienas-url'),
    path('modeliai/', views.ModelisListView.as_view(), name='modeliai-all-url'),
    path('modeliai/<int:pk>', views.ModelisDetailView.as_view(), name='modelis-vienas-url'),
    path('search/', views.search, name='search-url'),
    path('mano_uzsakymai', views.UzsakymaiByUserListView.as_view(), name='mano-uzsakymai'),
    path('register/', views.register, name='register-url'),
]