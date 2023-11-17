
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
        self.fields["returning_time"] = forms.ChoiceField(
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

    # VALIDATION

    def clean_departing_date(self):
        departing_date = self.cleaned_data.get("departing_date")
        if departing_date < datetime.date.today():
            raise forms.ValidationError("This date cannot be in the past")

        datediff = departing_date - datetime.date.today()
        days = datediff.days
        if days > 180:
            raise forms.ValidationError(
                        "This date cannot be more than 180 "
                        "days later than the Current Date")

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
                        "This date cannot be earlier than the Departing date")

        datediff = returning_date - departing_date
        days = datediff.days
        if days > 180:
            raise forms.ValidationError(
                        "This date cannot be more than 180 "
                        "days later than the Departing date")

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
                        "There must be at least one adult per booking")

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
                        "You cannot travel with more infants than adults")

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


class PassengerDetailsForm(forms.Form):  # TODO
    pass


# TODO
class PaxForm(forms.Form):
    pass


class BasePaxFormSet(BaseFormSet):
    #  TODO
    # def add_fields(self, form, index):
    #     super().add_fields(form, index)
    #     form.fields["body"] = forms.CharField()

    def clean(self):
        """
        Validation of the Adult, Children and Infants Formsets
        These formsets represent the Passenger Details Form
        """

        if any(self.errors):
            # Errors found - proceed no further
            return
        print(2000)
        theforms = self.forms
        if not theforms or not theforms[0].has_changed():
            raise forms.ValidationError("Please enter the details regarding "
                                        "the passengers for this booking.")
        count = 0
        for form in theforms:
            count += 1
            print("FORM>", count, form)
            print(form.cleaned_data, "CLEAN")

            # First Name Validation
            first_name = (form.cleaned_data.get("first_name", "")
                              .strip().upper()) #  TODO
            # print("FN", first_name)
            if not first_name:
                raise forms.ValidationError(
                        f"Adult {count} - Passenger Name required. "
                        f"Enter the First Name as on the passport")

            # Last Name Validation
            last_name = (form.cleaned_data.get("last_name", "")
                              .strip().upper())
            # print("FN", first_name)
            if not last_name:
                raise forms.ValidationError(
                        f"Adult {count} - Passenger Name required. "
                        f"Enter the Last Name as on the passport")

            # Contact TelNo/Email Validation
            phone_number = (form.cleaned_data.get("contact_number", "")
                                .strip())
            # TODO RE strip()
            phone_number = (form.cleaned_data.get("contact_number", "")
                                .replace(" ", ""))
            email = (form.cleaned_data.get("contact_email", "").strip())

            if not phone_number and not email:
                if count == 1:
                    raise forms.ValidationError(
                        f"Adult {count} is the Principal Passenger."
                        "Therefore, the Contact Details are "
                        "mandatory for this Passenger.\n"
                        "Please enter passenger's phone number or email")
                else:
                    continue

            if phone_number and not re.search("[0-9]{6,}", phone_number):
                raise forms.ValidationError(
                        f"Adult {count} - Contact number. "
                        f"Enter a phone number of at least 6 digits")

            # This solution found at https://stackoverflow.com/questions/3217682/how-to-validate-an-email-address-in-django
            if email:
                try:
                    validate_email(email)
                except ValidationError as e:
                    raise forms.ValidationError(
                               f"Adult {count} - Email. "
                               "Please enter a valid email address")


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
    title = forms.CharField(max_length=4,
                            widget=forms.Select(choices=Common.TITLE_CHOICES),
                            initial="MR",)
    first_name = forms.CharField(max_length=40, required=True)
    last_name = forms.CharField(max_length=40, required=True)
    contact_number = forms.CharField(max_length=40)
    contact_email = forms.CharField(max_length=40)
    wheelchair_ssr = forms.CharField(max_length=1)
    wheelchair_type = forms.CharField(max_length=1)

    # VALIDATION

    def clean_first_name(self):
        """ First Name Validation """
        first_name = trim(self.cleaned_data.get("first_name")).upper()
        print("FN", first_name)
        if not first_name:
            raise forms.ValidationError(
                        "Passenger Name required. "
                        "Enter the first last name as on the passport")

        return first_name

    def clean(self):
        print(type(self))
#       cleaned_data = super(BasePaxFormSet, self).clean()
#       print("CD", cleaned_data)
#       return cleaned_data
        """ First Name Validation """
        print(1000, type(self))
        print(self)
        for form in self.forms:
            print("FORM>", form)
        print(self.errors)
        return
        first_name = trim(self.cleaned_data.get("first_name")).upper()
        print("FN", first_name)
        if not first_name:
            raise forms.ValidationError(
                        "Passenger Name required. "
                        "Enter the first last name as on the passport")

        return first_name


# For Children and Infants
class MinorsForm(forms.Form):
    title = forms.CharField(max_length=4,
                            widget=forms.Select(choices=Common.TITLE_CHOICES),
                            initial="MR",)
    first_name = forms.CharField(max_length=40, required=True)
    last_name = forms.CharField(max_length=40, required=True)
    date_of_birth = forms.DateField(initial=datetime.date.today(),
                                    help_text="Format: DD/MM/YYYY",
                                    widget=forms.DateInput(
                                    attrs=dict(type="date")))
    wheelchair_ssr = forms.CharField(max_length=1)
    wheelchair_type = forms.CharField(max_length=1)
