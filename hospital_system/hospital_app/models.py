from symtable import Class

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Doctor(models.Model):
    full_name = models.CharField(max_length=200)
    SPECIALTY_CHOICES = [
        ("cardiologist", "Cardiologist"),
        ("dermatologist", "Dermatologist"),
        ("neurologist", "Neurologist")
    ]
    specialty = models.CharField(choices=SPECIALTY_CHOICES, max_length=20)
    image = models.ImageField(upload_to='doctors')
    institution = models.CharField(max_length=200)
    completed_appointments = models.IntegerField(default=0)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.full_name} ({self.specialty})"


class Patient(models.Model):
    full_name = models.CharField(max_length=200)
    birth_date = models.DateField(auto_now_add=False)
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female")
    ]
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    email = models.EmailField()
    institution = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.full_name


class Appointment(models.Model):
    TYPE_CHOICES = [
        ("cardiologist", "Cardiological"),
        ("dermatologist", "Dermatological"),
        ("neurologist", "Neurological")
    ]
    appointment_type = models.CharField(choices=TYPE_CHOICES, max_length=20)
    description = models.TextField()
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("in_progress", "In Progress"),
        ("completed", "Completed")
    ]
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="scheduled")
    datetime = models.DateTimeField(auto_now_add=False, auto_now=False)
    note = models.TextField(null=True, blank=True)
    patient = models.ForeignKey(to=Patient, on_delete=models.SET_NULL, null=True, blank=True)
    responsible_doctor = models.ForeignKey(to=Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.appointment_type} - {self.status}"


class AppointmentAssignment(models.Model):
    appointment = models.ForeignKey(to=Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(to=Doctor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("appointment", "doctor")

    def __str__(self):
        return f"{self.appointment} assisting {self.doctor}"
