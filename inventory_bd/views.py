from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View, generic
from django.views.generic import UpdateView, CreateView, FormView

from inventory_bd.models import Thing, Responsible
import sqlite3
from inventory_bd.forms import ThingForm, ResponsibleForm


class MainView(View):
    def get(self, request):
        return render(request, 'inventory_bd/main.html')


def bd_list(request, *args, **kwargs):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("""select id, name, code, inv, price, count, summ, note from inventory_bd_thing""")
    tables = cursor.fetchall()
    my_id = conn.cursor()
    my_id.execute("""select id from inventory_bd_thing""")
    qr = conn.cursor()
    qr.execute("""select id from inventory_bd_thing""")
    return render(request, 'inventory_bd/thing_table.html', {'tables': tables, 'my_id': my_id, 'qr': qr})


class QRView(View):
    def get(self, request, profile_id):
        thing = Thing.objects.get(id=profile_id)
        inventory_form = ThingForm(instance=thing)
        return render(request, 'inventory_bd/qrcode.html',
                      context={'inventory_form': inventory_form, 'profile_id': profile_id})

    def post(self, request, profile_id):
        thing = Thing.objects.get(id=profile_id)
        inventory_form = ThingForm(request.POST, instance=thing)

        return render(request, 'inventory_bd/qrcode.html',
                      context={'inventory_form': inventory_form, 'profile_id': profile_id})



class ThingCreateView(CreateView):
    model = Thing
    fields = ['name', 'code', 'inv', 'price', 'count', 'summ', 'note']

    def form_valid(self, form):
        Thing.objects.create(**form.cleaned_data)

        return HttpResponseRedirect(reverse('thing-list'))


class ThingUpdateView(UpdateView):
    model = Thing
    template_name_suffix = '_update_form'
    fields = ['name', 'code', 'inv', 'price', 'count', 'summ', 'note']

    def form_valid(self, form):
        form.save(commit=True)

        return HttpResponseRedirect(reverse('thing-list'))


class RespListView(generic.ListView):
    model = Responsible
    template_name = 'responsible_list.html'
    context_object_name = 'responsible_list'

def responsible_table(request, *args, **kwargs):
    things = Thing.objects.all()
    resp = Responsible.objects.all()


    return render(request, 'inventory_bd/responsible_all.html', {'things': things, 'resp': resp})


class RespUpdateView(UpdateView):
    model = Responsible
    template_name_suffix = '_update_form'
    fields = ['name', 'things']

    def form_valid(self, form):
        form.save(commit=True)

        return HttpResponseRedirect(reverse('resp-list'))


class RespCreateView(FormView):
    template_name = "inventory_bd/responsible_form.html"
    form_class = ResponsibleForm

    def form_valid(self, form):
        nm = form.cleaned_data.get('name')
        obj = form.cleaned_data.get('things')

        instance = Responsible.objects.create(name=nm)

        instance.things.add(*obj)
        return HttpResponseRedirect(reverse('resp-list'))



def general_list(request, *args, **kwargs):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("""select responsible_id, thing_id from inventory_bd_responsible_things""")
    general = cursor.fetchall()
    return render(request, 'inventory_bd/general_list.html', {'general': general})



