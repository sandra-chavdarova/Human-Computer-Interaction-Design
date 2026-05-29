# Define your signal receivers here.

from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .models import *
from django.utils import timezone


@receiver(pre_save, sender=Appointment)
def change_status(sender, instance, **kwargs):
    if instance.status == "completed" and instance.datetime > timezone.now():
        instance.status = "scheduled"

    if instance.status == "scheduled" and instance.datetime < timezone.now():
        instance.status = "completed"

    if instance.pk is None and instance.patient_id is not None:
        doctor = instance.responsible_doctor
        institution = instance.patient.institution
        patients = Appointment.objects.filter(responsible_doctor=doctor, patient__institution=institution).values_list(
            'patient_id', flat=True).distinct()
        if len(patients) >= 3:
            instance.note = f"High workload with patients from institution {institution}"


@receiver(post_save, sender=Appointment)
def increment_number(sender, instance, created, **kwargs):
    if instance.status == "completed":
        doctor = Doctor.objects.filter(id=instance.responsible_doctor.pk).first()
        if doctor:
            doctor.completed_appointments += 1
            doctor.save()


@receiver(pre_delete, sender=Patient)
def delete_patient(sender, instance, **kwargs):
    appointments = Appointment.objects.filter(patient=instance)
    for appointment in appointments:
        if appointment.status == "scheduled":
            appointment.delete()
        elif appointment.status == "in_progress":
            appointment.note = "Patient record missing – appointment preserved for audit purposes"
            appointment.save()
