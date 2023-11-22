from django.db import models

# Create your models here.


class Flight(models.Model):
    flight_number = models.CharField(max_length=6, primary_key=True)
    flight_from = models.CharField(max_length=3)
    flight_to = models.CharField(max_length=3)
    flight_STD = models.CharField(max_length=4)
    flight_STA = models.CharField(max_length=4)
    outbound = models.BooleanField(default=True)
    capacity = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["flight_number"]

    def __str__(self):
        return (f"{self.flight_number} "
                f"{self.flight_from} {self.flight_to} "
                f"{self.flight_STD} {self.flight_STA}")


class Schedule(models.Model):
    flight_date = models.DateField()
    flight_number = models.CharField(max_length=6)
    total_booked = models.PositiveSmallIntegerField()
    # Bit String which represents the seating of passengers
    seatmap = models.CharField(max_length=12, default="0" * 12)

    class Meta:
        ordering = ["flight_date", "flight_number"]

    def __str__(self):
        return "{0} {1} BOOKED TO {2} PAX".format(self.flight_number,
                                                  self.flight_date
                                                  .strftime("%d/%m/%Y"),
                                                  self.total_booked)


class Booking(models.Model):
    pnr = models.CharField(max_length=6, unique=True)
    created_at = models.DateField(auto_now=True)
    amended_at = models.DateField(auto_now_add=True)

    flight_from = models.CharField(max_length=3)
    flight_to = models.CharField(max_length=3)
    return_flight = models.BooleanField(default=True)

    # Outbound Date + Flight No (e.g. MX0485)
    outbound_date = models.DateField(auto_now=True)
    outbound_flightno = models.CharField(max_length=6, default="")
    # Inbound Date + Flight No (e.g. MX0486)
    # Optional i.e. One-Way Journey
    inbound_date = models.DateField(null=True)
    inbound_flightno = models.CharField(max_length=6, blank=True, default="")

    fare_quote = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    ticket_class = models.CharField(max_length=1, default="Y")
    cabin_class = models.CharField(max_length=1, default="Y")
    number_of_adults = models.PositiveSmallIntegerField(default=0)
    number_of_children = models.PositiveSmallIntegerField(default=0)
    number_of_infants = models.PositiveSmallIntegerField(default=0)
    number_of_bags = models.PositiveSmallIntegerField(default=0)
    departure_time = models.CharField(max_length=4)
    arrival_time = models.CharField(max_length=4)
    remarks = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["pnr"]

    def __str__(self):
        return_flight_info = ("{0} {1}"
                              .format(self.inbound_flightno,
                                      self.inbound_date.strftime("%d%b%Y")
                                          .upper())
                              if self.return_flight else "")

        adult_plural = "S" if self.number_of_adults != 1 else ""
        child_plural = "CHILDREN" if self.number_of_children != 1 else "CHILD"
        infant_plural = "S" if self.number_of_infants != 1 else ""
        return ("PNR: {0} {1} {2} {3} - {4} ADULT{5}, {6} {7} & {8} INFANT{9}".format(
                 self.pnr, # 0
                 self.outbound_flightno, # 1
                 self.outbound_date.strftime("%d%b%Y").upper(), # 2
                 return_flight_info, #3 
                 self.number_of_adults, #4
                 adult_plural, #5
                 self.number_of_children, #6
                 child_plural, #7
                 self.number_of_infants, # 8,
                 infant_plural)) #9


class Passenger(models.Model):
    title = models.CharField(max_length=3)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    # A=Adult C=Child I=Infant
    pax_type = models.CharField(max_length=1, default="A")
    # The passenger number within the Booking i.e.
    # 1st passenger is 1, 2nd is 2, etc
    pax_number = models.PositiveSmallIntegerField(default=1)
    # D.O.B. applicable to Children and Infants only
    date_of_birth = models.DateField(null=True)
    # Either one of these two fields needs to be set for Adult No. 1
    contact_number = models.CharField(max_length=40, blank=True, default="")
    contact_email = models.CharField(max_length=40, blank=True, default="")
    pnr = models.ForeignKey(Booking, on_delete=models.CASCADE)
    seat_number = models.PositiveSmallIntegerField(default=0)
    # Status: HK1 for PAX 1, HK2 for PAX 2, etc
    status = models.CharField(max_length=3)
    # Optional Wheelchair Info
    # Blank or R for WHCR, S for WCHS, C for WCHC
    wheelchair_ssr = models.CharField(max_length=1, blank=True, default="")
    # This field will only be set if 'wheelchair_ssr' is non-blank
    # M for WCMP, L for WCLB; D for WCBD; W for WCBW;
    # Blank - PAX not travelling with a wheelchair
    wheelchair_type = models.CharField(max_length=1, blank=True, default="")

    def __str__(self):
        return "{0} PAX: {1} {2} {3}".format(
            self.pnr, self.title, self.first_name, self.last_name)


class Transaction(models.Model):
    pnr = models.CharField(max_length=6)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    date_created = models.DateField()

    def __str__(self):
        return "{0} AMOUNT: {1} DATE CREATED {2}".format(
            self.pnr, self.amount,
            self.date_created.strftime("%Y%m%d"), self.flight_number)
