from django import forms
from DublinBusTest.models import *

class routeForm(forms.ModelForm):
    class Meta:
        model = Routes
        fields = ('route_short_name',)
