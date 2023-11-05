from django.db import models

# Create your models here.


class Employer(models.Model):
    company_name = models.CharField(max_length=45)
    number_of_employees = models.IntegerField()    
    employer_test_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

class Employee(models.Model):
    TITLES = [
        ("Mr", "Mister"),
        ("Ms", "Miss"),
        ("Mx", "Unspecified"),
    ]
    title = models.CharField(max_length=2, choices=TITLES)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)    
    employee_test_flag = models.BooleanField(default=False)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + ' ' + last_name
