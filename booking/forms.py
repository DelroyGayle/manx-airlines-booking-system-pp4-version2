
from django import forms
from .models import Employer


class BookingForm(forms.ModelForm):

    class Meta:
        model = Employer

        fields = '__all__'