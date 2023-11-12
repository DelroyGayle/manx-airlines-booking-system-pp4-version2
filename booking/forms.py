
from django import forms
from django.forms import BaseFormSet
from .models import Booking
import datetime


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = '__all__'


# creating a form
class CreateBookingForm(forms.Form):
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

    OUTBOUND_TIME_OPTIONS1 = ("0800",
                              "1330",
                              "1830")

    OUTBOUND_TIME_OPTIONS2 = ("08:00 LCY - 09:45 IOM",
                              "13:30 LCY - 15:15 IOM",
                              "18:30 LCY - 20:15 IOM")

    INBOUND_TIME_OPTIONS1 = ("1100",
                             "1600",
                             "2100")

    INBOUND_TIME_OPTIONS2 = ("11:00 IOM - 12:45 LCY",
                             "16:00 IOM - 17:45 LCY",
                             "21:00 IOM - 22:45 LCY")

    return_option = forms.ChoiceField(
        choices=RETURN_CHOICE,
    )

    departing_date = forms.DateField(initial=datetime.date.today()
                                     .strftime("%d/%m/%Y"),
                                     help_text="Format: DD/MM/YYYY",
                                     input_formats=["%d/%m/%Y"])

    the_choices = list(zip(OUTBOUND_TIME_OPTIONS1, OUTBOUND_TIME_OPTIONS2))
    departing_time = forms.ChoiceField(initial=OUTBOUND_TIME_OPTIONS1[0],
                                       choices=the_choices,
                                       widget=forms.RadioSelect)

    returning_date = forms.DateField(initial=datetime.date.today()
                                     .strftime("%d/%m/%Y"),
                                     help_text="Format: DD/MM/YYYY",
                                     input_formats=["%d/%m/%Y"])

    the_choices = list(zip(INBOUND_TIME_OPTIONS1, INBOUND_TIME_OPTIONS2))
    returning_time = forms.ChoiceField(initial=INBOUND_TIME_OPTIONS1[0],
                                       choices=the_choices,
                                       widget=forms.RadioSelect)

    adults = forms.IntegerField(initial=1, min_value=0, max_value=20)
    children = forms.IntegerField(initial=0, min_value=0, max_value=20)
    infants = forms.IntegerField(initial=0, min_value=0, max_value=20)


# TODO
class PassengerDetailsForm(forms.Form):
    pass


class PaxForm(forms.Form):
    pass


class BasePaxFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields['body'] = forms.CharField()


class AdultsForm(forms.Form):
    title = forms.CharField()
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    contact_number = forms.CharField(max_length=40)
    email = forms.CharField(max_length=40)
    wheelchair_ssr = forms.CharField(max_length=1)
    wheelchair_type = forms.CharField(max_length=1)


# Used also for Children and Infants
class MinorsForm(forms.Form):
    title = forms.CharField()
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    date_of_birth = forms.DateField()
    wheelchair_ssr = forms.CharField(max_length=1)
    wheelchair_type = forms.CharField(max_length=1)
