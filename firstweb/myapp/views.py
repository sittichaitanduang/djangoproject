from urllib import request

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import *


# Create your views here.
def Home(request):
    return render(request, 'home.html')

def About(request):
    return render(request, 'about.html')

def AllProducts(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'allproducts.html', context)


from .forms import UserRegisterForm
from django.contrib import messages
from django.shortcuts import render,redirect

def Register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'ยินดีต้อนรับ {username} บัญชีของคุณถูกสร้างแล้ว!')
            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('all-products')
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

from django.contrib.auth import logout as auth_logout
def logout(request):
    auth_logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required
@login_required
def profile(request):
   # ป้องกัน error สำหรับ User เก่าที่ยังไม่มี profile
   if not hasattr(request.user, 'profile'):
       Profile.objects.create(user=request.user)
   return render(request, 'profile.html')
