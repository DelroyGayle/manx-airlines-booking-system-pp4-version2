
from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = '__all__'


# creating a form   
class InputForm(forms.Form): 

    NUMBERS_1TO20 = [(i,)*2 for i in range(0,21)]
    RETURN = "Y"
    ONE_WAY = "N"
    RETURN_CHOICE = [
        (RETURN, "Return"),
        (ONE_WAY, "One Way")
    ]

    OUTBOUND_TIME_OPTIONS = ("08:00 LCY - 09:45 IOM",
                             "13:30 LCY - 15:15 IOM",
                             "18:30 LCY - 20:15 IOM")

    INBOUND_TIME_OPTIONS = ("11:00 IOM - 12:45 LCY",
                            "16:00 IOM - 17:45 LCY",
                            "21:00 IOM - 22:45 LCY")

    return_option = forms.ChoiceField(
        choices=RETURN_CHOICE,
    )

    departing_date = forms.DateField()

    departing_time = forms.ChoiceField(
        choices=list(zip(OUTBOUND_TIME_OPTIONS, OUTBOUND_TIME_OPTIONS)),
        widget=forms.RadioSelect,
    )

    returning_date = forms.DateField()

    returning_time = forms.ChoiceField(
        choices=list(zip(INBOUND_TIME_OPTIONS, INBOUND_TIME_OPTIONS)),
        widget=forms.RadioSelect,
    )

    adults = forms.ChoiceField(
        choices=NUMBERS_1TO20,
    )    
    children = forms.ChoiceField(
        choices=NUMBERS_1TO20,
    )    
    infants = forms.ChoiceField(
        choices=NUMBERS_1TO20,
    )    
