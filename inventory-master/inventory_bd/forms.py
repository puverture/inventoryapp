from django import forms
from inventory_bd.models import Responsible, Thing


class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing
        fields = '__all__'


class ResponsibleForm(forms.ModelForm):
    things = forms.ModelMultipleChoiceField(
        queryset=Thing.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Responsible
        fields = ['name', 'things']



