from django import forms
from .models import *


class MeasurementModelForm(forms.ModelForm):
	class Meta:
		model = Measurement
		fields = ('destination',)
