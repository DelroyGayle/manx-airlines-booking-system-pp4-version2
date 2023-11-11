
from django import forms
from .models import Booking
import datetime


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = '__all__'


# creating a form
class CreateBooking_Form(forms.Form):
    def as_p(self):
        """This method overrides the default 'as_p' behaviour
           because I did not like the way this form looked.
           This method returns this form rendered as HTML <p>s.
           Found this solution at
           https://stackoverflow.com/questions/7769805/editing-django-form-as-p
        """
        return self._html_output(
            normal_row=u'<p%(html_class_attr)s>%(label)s</p>'
            u'%(field)s%(help_text)s',
            error_row=u'%s',
            row_ender='</p>',
            help_text_html=u'<br><span class="helptext">%s</span>',
            errors_on_separate_row=True)

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

    departing_date = forms.DateField(initial=datetime.date.today()
                                     .strftime("%d/%m/%Y"),
                                     help_text="Format: DD/MM/YYYY",
                                     input_formats=["%d/%m/%Y"])

    the_choices = list(zip(OUTBOUND_TIME_OPTIONS, OUTBOUND_TIME_OPTIONS))
    departing_time = forms.ChoiceField(initial=OUTBOUND_TIME_OPTIONS[0],
                                       choices=the_choices,
                                       widget=forms.RadioSelect)

    returning_date = forms.DateField(initial=datetime.date.today()
                                     .strftime("%d/%m/%Y"),
                                     help_text="Format: DD/MM/YYYY",
                                     input_formats=["%d/%m/%Y"])

    the_choices = list(zip(INBOUND_TIME_OPTIONS, INBOUND_TIME_OPTIONS))
    returning_time = forms.ChoiceField(initial=INBOUND_TIME_OPTIONS[0],
                                       choices=the_choices,
                                       widget=forms.RadioSelect)

    adults = forms.IntegerField(initial=0, min_value=0, max_value=20)
    children = forms.IntegerField(initial=0, min_value=0, max_value=20)
    infants = forms.IntegerField(initial=0, min_value=0, max_value=20)
