from django.shortcuts import render, redirect

from .forms import AppointmentForm
from .models import *
from django.utils import timezone


# Create your views here.

def index(request):
    cardiologists = Doctor.objects.filter(specialty="cardiologist")
    dermatologists = Doctor.objects.filter(specialty="dermatologist")
    neurologists = Doctor.objects.filter(specialty="neurologist")
    context = {"cardiologists": cardiologists, "dermatologists": dermatologists, "neurologists": neurologists}
    return render(request, 'index.html', context)


def doctor_detail(request, doctor_id):
    doctor = Doctor.objects.filter(id=doctor_id).first()
    if not doctor:
        from django.http import Http404
        raise Http404
    appointment_ids = AppointmentAssignment.objects.filter(doctor=doctor).values_list('appointment', flat=True)
    appointments = Appointment.objects.filter(models.Q(id__in=appointment_ids) |
                                              models.Q(responsible_doctor=doctor)).distinct()
    past = appointments.filter(datetime__lt=timezone.now())
    today = appointments.filter(datetime__date=timezone.now().date())
    future = appointments.filter(datetime__gt=timezone.now())
    if request.method == "POST":
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.appointment_type = doctor.specialty
            app.responsible_doctor = doctor
            app.save()
            AppointmentAssignment.objects.create(appointment=app, doctor=doctor)
            return redirect('doctor_detail', doctor_id=doctor.id)
    form = AppointmentForm()
    context = {"doctor": doctor, "past_appointments": past, "today_appointments": today, "future_appointments": future,
               "form": form}
    return render(request, 'details.html', context)
