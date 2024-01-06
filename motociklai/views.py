from django.shortcuts import render, get_object_or_404, redirect, reverse
# from django.http import HttpResponse
from django.views import generic
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Gamintojas, Modelis, ModelisInstance
from .forms import ModelisReviewForm, UserUpdateForm, ProfilisUpdateForm


# Create your views here.


def index(request):
    num_gamintoju = Gamintojas.objects.all().count()
    num_instances = ModelisInstance.objects.all().count()
    num_modeliu = Modelis.objects.count()
    num_instances_available = ModelisInstance.objects.filter(status__exact='t').count()

    username = request.user

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context_t = {
        'num_gamintojas_t': num_gamintoju,
        'num_instances_t': num_instances,
        'num_modelis_t': num_modeliu,
        'num_instances_available_t': num_instances_available,
        'username_t': username,
        'num_visits_t': num_visits
    }

    return render(request, 'index.html', context=context_t)


def gamintojai(request):
    paginator = Paginator(Gamintojas.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_gamintojai = paginator.get_page(page_number)
    context_t = {
        'gamintojai_t': paged_gamintojai
    }
    return render(request, 'gamintojai_visi.html', context=context_t)


def gamintojas(request, gamintojas_id):
    gamintojas_viena_eilute = get_object_or_404(Gamintojas, pk=gamintojas_id)
    context_t = {
        'gamintojas_viena_eilute_t': gamintojas_viena_eilute
    }
    return render(request, 'gamintojas_vienas.html', context=context_t)


class ModelisListView(generic.ListView):
    model = Modelis
    context_object_name = 'modelis_list'
    template_name = 'modeliai_list.html'
    paginate_by = 3


class ModelisDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Modelis
    context_object_name = 'modelis'
    template_name = 'modelis_detail.html'
    form_class = ModelisReviewForm

    def get_success_url(self):
        return reverse('modelis-vienas-url', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.modelis = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)


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


class UzsakymaiByUserListView(LoginRequiredMixin, generic.list.ListView):
    model = ModelisInstance
    template_name = "mano-uzsakymai.html"
    context_object_name = 'modelisinstance_list'

    def get_queryset(self):
        return ModelisInstance.objects.filter(klientas=self.request.user)


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f"Vartotojo vardas {username} uzimtas!"),

                return redirect('register-url')

            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"Vartotojas su email adresu {email} egzistuoja!")
                    return redirect('register-url')
                else:

                    User.objects.create_user(username=username, email=email, password=password)
                    messages.success(request, f"Vartotojas {username} sukurtas!!!")
                    return redirect('login')

    else:
        return render(request, "registration/registration.html")


@login_required
def profilis(request):
    if request.method == "GET":
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)
    elif request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, ("Your profile was updated"))
            return redirect('profilis-url')
    context_t = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profilis.html', context=context_t)

