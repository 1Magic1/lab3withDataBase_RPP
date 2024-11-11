from django.shortcuts import redirect
from .models import Profile

def doctor_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('doctor_login')  # Перенаправляє на сторінку авторизації лікаря
        
        profile = Profile.objects.filter(user=request.user).first()
        if profile is None or profile.role != 'doctor':
            return redirect('home')  # Або сторінка з повідомленням про помилку

        return view_func(request, *args, **kwargs)
    return _wrapped_view

def pharmacist_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        if profile.role != 'pharmacist':
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
