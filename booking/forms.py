
from django import forms
from django.forms import BaseFormSet
from .models import Booking
from .common import Common
import datetime


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = "__all__"


# creating a form
class CreateBookingForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(CreateBookingForm, self).__init__(*args, **kwargs)

        # Finally found the solution to how to update choice fields here:
        # https://stackoverflow.com/questions/24877686/update-django-choice-field-with-database-results
        the_choices = list(zip(Common.OUTBOUND_TIME_OPTIONS1,
                               Common.OUTBOUND_TIME_OPTIONS2))
        self.fields['departing_time'] = forms.ChoiceField(
                    initial=Common.OUTBOUND_TIME_OPTIONS1[0],
                    choices=the_choices, widget=forms.RadioSelect)

        the_choices = list(zip(Common.INBOUND_TIME_OPTIONS1,
                               Common.INBOUND_TIME_OPTIONS2))
        self.fields['returning_time'] = forms.ChoiceField(
                    initial=Common.INBOUND_TIME_OPTIONS1[0],
                    choices=the_choices, widget=forms.RadioSelect)

    def as_p(self):
        """This method overrides the default 'as_p' behaviour
           because I did not like the way this form looked.
           This method returns this form rendered as HTML <p>s.
           Found this solution at
           https://stackoverflow.com/questions/7769805/editing-django-form-as-p
        """
        return self._html_output(
            normal_row=u"<p%(html_class_attr)s>%(label)s</p>"
            u"%(field)s%(help_text)s",
            error_row=u"%s",
            row_ender="</p>",
            help_text_html=u"<br><span class='helptext'>%s</span>",
            errors_on_separate_row=True)

    def clean_departing_date(self):
        departing_date = self.cleaned_data.get("departing_date")
        if departing_date < datetime.date.today():
            raise forms.ValidationError("This date cannot be in the past")

        return departing_date

    def clean_returning_date(self):
        returning_date = self.cleaned_data.get("returning_date")
        departing_date = self.cleaned_data.get("departing_date")
        if self.cleaned_data.get("departing_date") == "Y":
            if returning_date < departing_date:
                raise forms.ValidationError(
                        "This date cannot be earlier than the Departing date")
            datediff = returning_date - departing_date
            days = datediff.days
            if days > 180:
                raise forms.ValidationError(
                        "This date cannot be more than 180 "
                        "days later than the Departing date")

        return returning_date

    RETURN = "Y"
    ONE_WAY = "N"
    RETURN_CHOICE = [
        (RETURN, "Return"),
        (ONE_WAY, "One Way")
    ]

    return_option = forms.ChoiceField(
        choices=RETURN_CHOICE,
    )

    departing_date = forms.DateField(initial=datetime.date.today(),
                                     help_text="Format: DD/MM/YYYY",
                                     widget=forms.DateInput(
                                                 attrs=dict(type='date')))

    departing_time = forms.ChoiceField(widget=forms.RadioSelect)

    returning_date = forms.DateField(initial=datetime.date.today(),
                                     help_text="Format: DD/MM/YYYY",
                                     widget=forms.DateInput(
                                                  attrs=dict(type='date')))

    returning_time = forms.ChoiceField(widget=forms.RadioSelect)

    # TODO
    adults = forms.IntegerField(initial=1, min_value=1, max_value=20)
    children = forms.IntegerField(initial=0, min_value=0, max_value=20)
    infants = forms.IntegerField(initial=0, min_value=0, max_value=20)


class PassengerDetailsForm(forms.Form):  # TODO
    pass


# TODO
class PaxForm(forms.Form):
    pass


# TODO
class BasePaxFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields["body"] = forms.CharField()


class HiddenForm(forms.Form):
    return_option = forms.CharField(max_length=1, widget=forms.HiddenInput())
    departing_date = forms.DateField(input_formats=["%d/%m/%Y"],
                                     widget=forms.HiddenInput())
    departing_time = forms.CharField(max_length=4, widget=forms.HiddenInput())
    returning_date = forms.DateField(input_formats=["%d/%m/%Y"],
                                     widget=forms.HiddenInput())
    returning_time = forms.CharField(max_length=4, widget=forms.HiddenInput())
    adults = forms.IntegerField(widget=forms.HiddenInput())
    children = forms.IntegerField(widget=forms.HiddenInput())
    infants = forms.IntegerField(widget=forms.HiddenInput())


class AdultsForm(forms.Form):
    title = forms.CharField()
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    contact_number = forms.CharField(max_length=40)
    contact_email = forms.CharField(max_length=40)
    wheelchair_ssr = forms.CharField(max_length=1)
    wheelchair_type = forms.CharField(max_length=1)


# For Children and Infants
class MinorsForm(forms.Form):
    title = forms.CharField()
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    date_of_birth = forms.DateField()
    wheelchair_ssr = forms.CharField(max_length=1)
    wheelchair_type = forms.CharField(max_length=1)
