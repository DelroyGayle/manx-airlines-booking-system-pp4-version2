
from django import forms
from django.forms import BaseFormSet
from .models import Booking
from .common import Common
from django.core.validators import validate_email
import datetime
import re


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
        self.fields["departing_time"] = forms.ChoiceField(
                    initial=Common.OUTBOUND_TIME_OPTIONS1[0],
                    choices=the_choices, widget=forms.RadioSelect)

        the_choices = list(zip(Common.INBOUND_TIME_OPTIONS1,
                               Common.INBOUND_TIME_OPTIONS2))
    # Common.INBOUND_TIME_OPTIONS1[0] would be an interval 
    # of less than 90 minutes. Therefore use the next available slot
    # i.e. Common.INBOUND_TIME_OPTIONS1[1]
        self.fields["returning_time"] = forms.ChoiceField(
                    initial=Common.INBOUND_TIME_OPTIONS1[1],
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

    # VALIDATION

    def clean_departing_date(self):
        departing_date = self.cleaned_data.get("departing_date")
        if departing_date < datetime.date.today():
            raise forms.ValidationError("This date cannot be in the past.")

        datediff = departing_date - datetime.date.today()
        days = datediff.days
        if days > 180:
            raise forms.ValidationError(
                        "This date cannot be more than 180 "
                        "days later than the Current Date.")

        return departing_date

    def clean_returning_date(self):
        returning_date = self.cleaned_data.get("returning_date")
        if self.cleaned_data.get("return_option") == "N":
            # One Way Journey
            return returning_date

        departing_date = self.cleaned_data.get("departing_date")
        if not departing_date:
            # An error has already been determined -- use current date
            return datetime.date.today()

        if returning_date < departing_date:
            raise forms.ValidationError(
                        "This date cannot be earlier than the Departing date.")

        datediff = returning_date - departing_date
        days = datediff.days
        if days > 180:
            raise forms.ValidationError(
                        "This date cannot be more than 180 "
                        "days later than the Departing date.")

        return returning_date

    def clean_adults(self):
        """
        Defensive Programming
        The definition of this field has a 'min' value of one
        so it should never be zero
        Nonetheless just in case
        """
        number_of_adults = self.cleaned_data.get("adults")
        if number_of_adults <= 0:
            raise forms.ValidationError(
                        "There must be at least one adult per booking.")

        return number_of_adults

    def clean_infants(self):
        """
        Defensive Programming
        The field is validated server-side
        using JavaScript to ensure Infants <= Adults
        Nonetheless just in case
        """
        number_of_infants = self.cleaned_data.get("infants")
        number_of_adults = self.cleaned_data.get("adults")
        if not number_of_adults:
            # An error has already been determined - abort validation
            return number_of_infants
        if number_of_infants > number_of_adults:
            raise forms.ValidationError(
                        "You cannot travel with more infants than adults.")

        return number_of_infants

    ######################################################################
    # Initialisations

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
                                                 attrs=dict(type="date")))

    departing_time = forms.ChoiceField(widget=forms.RadioSelect)

    returning_date = forms.DateField(initial=datetime.date.today(),
                                     help_text="Format: DD/MM/YYYY",
                                     widget=forms.DateInput(
                                                  attrs=dict(type="date")))

    returning_time = forms.ChoiceField(widget=forms.RadioSelect)

    adults = forms.IntegerField(initial=1, min_value=1, max_value=20)
    children = forms.IntegerField(initial=0, min_value=0, max_value=20)
    infants = forms.IntegerField(initial=0, min_value=0, max_value=20)


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


TITLE_CHOICES = [
        ("DR", "DOCTOR"),
        ("INF", "INFANT"),
        ("LADY", "LADY"),
        ("LORD", "LORD"),
        ("MSTR", "MASTER"),
        ("MISS", "MISS"),
        ("MR", "MR"),
        ("MRS", "MRS"),
        ("MS", "MS"),
        ("PROF", "PROFESSOR"),
        ("SIR", "SIR"),
        ("SIS", "SISTER"),
    ]


PRM_CHOICES = (
    ("", "No"),
    ("R", "WCHR"),
    ("S", "WCHS"),
    ("C", "WCHC"),
)

WCH_CHOICES = (
    ("", "None"),
    ("M", "WCMP"),
    ("L", "WCLB"),
    ("D", "WCBD"),
    ("W", "WCBW"),
)


class AdultsForm(forms.Form):
    title = forms.CharField(max_length=4,
                            widget=forms.Select(choices=TITLE_CHOICES),
                            initial="MR")
    first_name = forms.CharField(max_length=40, required=False)
    last_name = forms.CharField(max_length=40, required=False)
    contact_number = forms.CharField(max_length=40, required=False)
    contact_email = forms.CharField(max_length=40, required=False)
    wheelchair_ssr = forms.CharField(max_length=1,  required=False,
                                     widget=forms.Select(choices=PRM_CHOICES),
                                     initial="")
    wheelchair_type = forms.CharField(max_length=1, required=False,
                                      widget=forms.Select(choices=WCH_CHOICES),
                                      initial="")

    # VALIDATION  TODO REMOVE

    def clean(self):
        print(type(self))
        print("CLEANEDxxx", self.cleaned_data)
        cleaned_data = self.cleaned_data
        # ## print(self)  TODO
        # print("TESTING adult-TOTAL_FORMS", self['adult-TOTAL_FORMS'])
        # return cleaned_data
        if False and 'first_name' not in cleaned_data:
            print("SEE")
            raise forms.ValidationError(
                        "Passenger Name required. "
                        "Enter the first name as on the passport.")
        if False and 'last_name' not in cleaned_data:
            raise forms.ValidationError(
                        "Passenger Name required. "
                        "Enter the last name as on the passport.")
        print("RETURNED", cleaned_data)  # TODO
        return cleaned_data


# For Children
class ChildForm(forms.Form):
    title = forms.CharField(max_length=4,
                            widget=forms.Select(choices=TITLE_CHOICES),
                            initial="MR",)
    first_name = forms.CharField(max_length=40, required=False)
    last_name = forms.CharField(max_length=40, required=False)
    date_of_birth = forms.DateField(required=False,
                                    initial=datetime.date.today(),
                                    help_text="Format: DD/MM/YYYY",
                                    widget=forms.DateInput(
                                    attrs=dict(type="date")))
    wheelchair_ssr = forms.CharField(max_length=1,  required=False,
                                     widget=forms.Select(choices=PRM_CHOICES),
                                     initial="")
    wheelchair_type = forms.CharField(max_length=1, required=False,
                                      widget=forms.Select(choices=WCH_CHOICES),
                                      initial="")


"""This class is used for the entry of the number of bags
Remarks regarding the Booking
"""
class BagRemarks(forms.Form):
    bags = forms.IntegerField(required=False, initial=0,
                             min_value=0, max_value=20)
    remarks = forms.CharField(required=False,
                              widget=forms.Textarea(
                                attrs={ "rows": "4" }))
