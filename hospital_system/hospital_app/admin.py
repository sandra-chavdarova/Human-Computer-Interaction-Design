from django.contrib import admin
from django.db.models import Q

from .models import *


# Register your models here.

class DoctorAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser


class PatientAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("appointment_type", "status", "datetime", "patient", "responsible_doctor")

    def has_add_permission(self, request):
        return request.user.is_superuser or Doctor.objects.filter(user=request.user).exists()

    def save_model(self, request, obj, form, change):
        if not change:
            doctor = Doctor.objects.filter(user=request.user).first()
            obj.user = request.user
            obj.responsible_doctor = doctor
        return super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            doctor = Doctor.objects.filter(user=request.user).first()
            if doctor:
                return obj.responsible_doctor == doctor
        return False

    def has_delete_permission(self, request, obj=None):
        return obj and obj.status == "scheduled"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        qs_doctors = Doctor.objects.filter(user=request.user)
        if not qs_doctors.exists():
            return qs.none()
        doctor = qs_doctors.first()
        return qs.filter(Q(responsible_doctor=doctor) | Q(appointmentassignment__doctor=doctor)).distinct()


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(AppointmentAssignment)
