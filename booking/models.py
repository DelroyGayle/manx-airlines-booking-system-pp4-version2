from django.db import models

# Create your models here.


class Flight(models.Model):
    flight_number = models.CharField(max_length=6, primary_key=True)
    flight_from = models.CharField(max_length=3)
    flight_to = models.CharField(max_length=3)
    flight_STD = models.CharField(max_length=4)
    capacity = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["flight_number"]

    def __str__(self):
        return self.flight_number


class Schedule(models.Model):
    flight_date = models.DateField()
    flight_number = models.CharField(max_length=6)
    total_booked = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["flight_date", "flight_number"]

    def __str__(self):
        return "{0}{1}".format(self.flight_date.strftime("%Y%m%d"),
                               self.flight_number)


class Booking(models.Model):
    pnr = models.CharField(max_length=6, unique=True)
    flight_from = models.CharField(max_length=3)
    flight_to = models.CharField(max_length=3)
    return_flight = models.BooleanField(default=True)
    # Outbound Date (YYYYMMDD) + Flight No (e.g. MX0485)
    outbound = models.CharField(max_length=14)
    # Inbound Date (YYYYMMDD) + Flight No (e.g. MX0486)
    inbound = models.CharField(max_length=14, blank=True, default="")
    fare_quote = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    ticket_class = models.CharField(max_length=1, default="Y")
    cabin_class = models.CharField(max_length=1, default="Y")
    number_of_pax = models.PositiveSmallIntegerField(default=0)
    number_of_infants = models.PositiveSmallIntegerField(default=0)
    number_of_bags = models.PositiveSmallIntegerField(default=0)
    departure_time = models.CharField(max_length=4)
    arrival_time = models.CharField(max_length=4)
    # Either one of these two fields needs to be set
    principal_contact_number = models.CharField(max_length=40, blank=True,
                                                default="")
    principal_email = models.CharField(max_length=40, blank=True, default="")
    remarks = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["pnr"]

    def __str__(self):
        return ("PNR: {0} ROUTE: {1}{2} JOURNEY: {3} - {4} "
                "PAX + {5} INFANTS".format(
                 self.pnr, self.flight_from, self.flight_to,
                 f"{self.outbound} {self.inbound}",
                 self.number_of_pax, self.number_of_infants))


class Passenger(models.Model):
    title = models.CharField(max_length=3)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    # A=Adult C=Child I=Infant
    pax_type = models.CharField(max_length=1, default="A")
    pax_order_number = models.PositiveSmallIntegerField(default=1)
    # D.O.B. applicable to Children and Infants only
    date_of_birth = models.DateField(null=True)
    # Either one of these two fields needs to be set for Adult No. 1
    # is used to populate either
    # 'principal_contact_number' or 'principal_email'
    # So, Either one of these two fields below needs to be set
    contact_number = models.CharField(max_length=40, blank=True, default="")
    contact_email = models.CharField(max_length=40, blank=True, default="")
    pnr = models.ForeignKey(Booking, on_delete=models.CASCADE)
    seat_number = models.PositiveSmallIntegerField(default=0)
    # Status: HK1 for PAX 1, HK2 for PAX 2, etc
    status = models.CharField(max_length=3)
    ticket_class = models.CharField(max_length=1, default="Y")
    # Optional Wheelchair Info
    # Blank or R for WHCR, S for WCHS, C for WCHC
    wheelchair_ssr = models.CharField(max_length=1, blank=True, default="")
    # This field will only be set if 'wheelchair_ssr' is non-blank
    # M for WCMP, L for WCLB; Blank - PAX not travelling with a wheelchair
    wheelchair_type = models.CharField(max_length=1, blank=True, default="")

    def __str__(self):
        return "PNR: {0} PAX: {1} {2} {3}".format(
            self.pnr, self.title, self.first_name, self.last_name)


class Transactions(models.Model):
    pnr = models.CharField(max_length=6)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    date_created = models.DateField()

    def __str__(self):
        return "PNR: {0} AMOUNT: {1} DATE CREATED {2}".format(
            self.pnr, self.amount,
            self.date_created.strftime("%Y%m%d"), self.flight_number)
