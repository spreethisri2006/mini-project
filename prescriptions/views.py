
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Prescription
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

import csv
from django.http import HttpResponse


def logout_view(request):
    logout(request)
    return redirect('login')
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(
                request,
                'Invalid username or password!'
            )

    return render(request, 'prescriptions/login.html')
@login_required(login_url='login')


def home(request):
    query = request.GET.get('search', '')
    selected_date = request.GET.get('date', '')

    prescriptions = Prescription.objects.all().order_by('-prescription_date')

    if query:
        prescriptions = prescriptions.filter(
            Q(patient_name__icontains=query) |
            Q(doctor_name__icontains=query) |
            Q(disease__icontains=query)|
            Q(medicines__icontains=query)
        )

    if selected_date:
        prescriptions = prescriptions.filter(
            prescription_date=selected_date
        )

    return render(request, 'prescriptions/home.html', {
        'prescriptions': prescriptions,
        'query': query,
        'selected_date': selected_date,
        'total_prescriptions': Prescription.objects.count(),
        'total_patients': Prescription.objects.values('patient_name').distinct().count(),
        'total_doctors': Prescription.objects.values('doctor_name').distinct().count(),
    })

@login_required(login_url='login')
def patient_history(request, patient_name):
    prescriptions = Prescription.objects.filter(
        patient_name__iexact=patient_name
    ).order_by('-prescription_date')

    return render(request, 'prescriptions/patient_history.html', {
        'patient_name': patient_name,
        'prescriptions': prescriptions
    })


   
@login_required(login_url='login')
def add_prescription(request):
    if request.method == 'POST':
        Prescription.objects.create(
            patient_name=request.POST['patient_name'],
            doctor_name=request.POST['doctor_name'],
            disease=request.POST['disease'],
            prescription_date=request.POST['prescription_date'],
            medicines=request.POST['medicines'],
            notes=request.POST.get('notes', '')
        )
        messages.success(request, 'Prescription added successfully!')
        return redirect('home')

    return render(request, 'prescriptions/add_prescription.html')

@login_required(login_url='login')
def edit_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)

    if request.method == 'POST':
        prescription.patient_name = request.POST['patient_name']
        prescription.doctor_name = request.POST['doctor_name']
        prescription.disease = request.POST['disease']
        prescription.prescription_date = request.POST['prescription_date']
        prescription.medicines = request.POST['medicines']
        prescription.notes = request.POST.get('notes', '')
        prescription.save()
        messages.success(request, 'Prescription updated successfully!')
        return redirect('home')

    return render(request, 'prescriptions/edit_prescription.html', {
        'prescription': prescription
    })

@login_required(login_url='login')
def delete_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)

    if request.method == 'POST':
        prescription.delete()
        messages.success(request, 'Prescription deleted successfully!')
        return redirect('home')

    return render(request, 'prescriptions/delete_prescription.html', {
        'prescription': prescription
    })

@login_required(login_url='login')
def export_prescriptions(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        'attachment; filename="prescriptions.csv"'
    )

    writer = csv.writer(response)
    writer.writerow([
        'Patient Name',
        'Doctor Name',
        'Disease',
        'Date',
        'Medicines',
        'Notes'
    ])

    prescriptions = Prescription.objects.all().order_by(
        '-prescription_date'
    )

    for prescription in prescriptions:
        writer.writerow([
            prescription.patient_name,
            prescription.doctor_name,
            prescription.disease,
            prescription.prescription_date,
            prescription.medicines,
            prescription.notes
        ])

    return response

