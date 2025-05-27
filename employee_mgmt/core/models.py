from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    education_details = models.TextField()
    salary = models.FloatField()
    date_joined = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    employee_details = models.TextField()

    def __str__(self):
        return self.user.username
