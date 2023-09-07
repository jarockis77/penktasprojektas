
from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from django.views import generic
from django.db.models import Q


from .models import Gamintojas, Modelis, Likutis, ModelisInstance
# Create your views here.


def index(request):
    num_gamintoju = Gamintojas.objects.all().count()
    num_instances = ModelisInstance.objects.all().count()
    num_modeliu = Modelis.objects.count()
    num_instances_available = ModelisInstance.objects.filter(status__exact='t').count()

    context_t = {
        'num_gamintojas_t': num_gamintoju,
        'num_instances_t': num_instances,
        'num_modelis_t': num_modeliu,
        'num_instances_available_t': num_instances_available,
    }

    return render(request, 'index.html', context=context_t)

def gamintojai(request):
    gamintojai_visos_eilutes = Gamintojas.objects.all()
    # print(authors)
    context_t = {
        'gamintojai_visos_eilutes_t': gamintojai_visos_eilutes
    }
    return render(request, 'gamintojai_visi.html', context=context_t)


def gamintojas(request, gamintojas_id):
    gamintojas_viena_eilute = get_object_or_404(Gamintojas, pk=gamintojas_id)
    context_t = {
        'gamintojas_viena_eilute_t': gamintojas_viena_eilute
    }
    return render(request, 'gamintojas_vienas.html', context=context_t)

class ModelisListView(generic.ListView):# ListView - visos eilutes is lenteles(objektai)
    model = Modelis #modelio klase_list --> book_list pasidaro pistoletiskai
    context_object_name = 'modelis_list' #nereikalingas jei nekeiciam pavadinimo
    template_name = 'modeliai_list.html'

class ModelisDetailView(generic.DetailView):
    model = Modelis
    context_object_name = 'modelis'
    template_name = 'modelis_detail.html'

def search(request):
    paieskos_tekstas = request.GET.get('search_text')
    paieskos_rezultatai = Modelis.objects.filter(
        Q(modelis__icontains=paieskos_tekstas) |
        Q(gamintojas__pavadinimas__icontains=paieskos_tekstas)
    )

    context_t = {
        'paieskos_tekstas_t': paieskos_tekstas,
        'paieskos_rezultatai_t': paieskos_rezultatai
    }
    return render(request, 'paieskos-rezultatai.html', context=context_t)