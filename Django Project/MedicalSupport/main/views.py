from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from .forms import PharmacistRegistrationForm
from .forms import PharmacistLoginForm
from .forms import DoctorRegistrationForm, DoctorLoginForm


def register_pharmacist(request):
    if request.method == 'POST':
        form = PharmacistRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Авторизуємо користувача після реєстрації
            return redirect('pharmacist_view')
    else:
        form = PharmacistRegistrationForm()
    return render(request, 'register_pharmacist.html', {'form': form})

def login_pharmacist(request):
    if request.method == 'POST':
        form = PharmacistLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('pharmacist_view')
    else:
        form = PharmacistLoginForm()
    return render(request, 'login_pharmacist.html', {'form': form})

def logout_pharmacist(request):
    logout(request)  # Вихід користувача
    return redirect('home')  # Перенаправлення на домашню сторінку або будь-яку іншу

def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Авторизація після реєстрації
            return redirect('doctor_view', doctor_id=user.id)
    else:
        form = DoctorRegistrationForm()
    return render(request, 'register_doctor.html', {'form': form})

def login_doctor(request):
    if request.method == 'POST':
        form = DoctorLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('doctor_view', doctor_id=user.id)
    else:
        form = DoctorLoginForm()
    return render(request, 'login_doctor.html', {'form': form})

# Дані пацієнтів, лікарів, аптекарів та рецептів
patients = {
    'patient1': {'name': 'Іван', 'medical_card': 'Хворіє на ГРВІ', 'info': 'Спортсмен'},
    'patient2': {'name': 'Марія', 'medical_card': 'Алергія на пилок', 'info': 'Викладач'},
    'patient3': {'name': 'Олексій', 'medical_card': 'Проблеми з серцем', 'info': 'Пенсіонер'},
    'patient4': {'name': 'Світлана', 'medical_card': 'Цукровий діабет', 'info': 'Бухгалтер'},
}

doctors = {
    'doctor1': {'name': 'Олена', 'specialty': 'Терапевт'},
    'doctor2': {'name': 'Андрій', 'specialty': 'Кардіолог'},
    'doctor3': {'name': 'Марина', 'specialty': 'Ендокринолог'},
}

pharmacists = {
    'pharmacist1': {'name': 'Сергій'},
    'pharmacist2': {'name': 'Людмила'},
    'pharmacist3': {'name': 'Петро'},
}

prescriptions = [
    {'patient': 'patient1', 'doctor': 'doctor1', 'medicine': 'Антибіотик', 'quantity': 1, 'sold': False},
    {'patient': 'patient2', 'doctor': 'doctor1', 'medicine': 'Антигістамін', 'quantity': 2, 'sold': False},
    {'patient': 'patient3', 'doctor': 'doctor2', 'medicine': 'Кардіопротектор', 'quantity': 1, 'sold': False},
    {'patient': 'patient4', 'doctor': 'doctor3', 'medicine': 'Інсулін', 'quantity': 3, 'sold': False},
]


def home_view(request):
    return render(request, 'home.html')

def patient_list(request):
    return render(request, 'patient_list.html', {'patients': patients})

def patient_view(request, patient_id):
    patient = patients.get(patient_id)
    if not patient:
        return redirect('patient_list')  # Повертає до списку, якщо пацієнт не знайдений
    return render(request, 'patient_view.html', {'patient': patient, 'patient_id': patient_id})

def update_patient_info(request, patient_id):
    if request.method == 'POST':
        patients[patient_id]['info'] = request.POST.get('info')
        return redirect('patient_view', patient_id=patient_id)
    return render(request, 'update_patient_info.html', {'patient_id': patient_id})

@login_required
def doctor_view(request, doctor_id):
    return render(request, 'doctor_view.html', {'doctor': doctors[doctor_id], 'patients': patients})

def create_prescription(request, doctor_id, patient_id):
    if request.method == 'POST':
        medicine = request.POST.get('medicine')
        quantity = request.POST.get('quantity')
        prescriptions.append({'patient': patient_id, 'doctor': doctor_id, 'medicine': medicine, 'quantity': quantity})
        return redirect('doctor_view', doctor_id=doctor_id)
    return render(request, 'create_prescription.html', {'doctor_id': doctor_id, 'patient_id': patient_id})

@login_required
def pharmacist_view(request):
    return render(request, 'pharmacist_view.html', {'prescriptions': prescriptions})

def update_medical_card(request, doctor_id, patient_id):
    patient = patients.get(patient_id)
    if request.method == 'POST':
        patient['medical_card'] = request.POST.get('medical_card')
        return redirect('doctor_view', doctor_id=doctor_id)
    return render(request, 'update_medical_card.html', {'doctor_id': doctor_id, 'patient': patient})

def sell_medicine(request, prescription_index):
    # Перевірка на наявність індексу рецепта
    if 0 <= prescription_index < len(prescriptions):
        prescriptions[prescription_index]['sold'] = True  # Встановлюємо статус "продано"
    return redirect('pharmacist_view')