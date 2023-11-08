from django.db import models

# Create your models here.


class Employer(models.Model):
    company_name = models.CharField(max_length=45)
    number_of_employees = models.IntegerField()    
    employer_test_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name


class Employee(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)    
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
