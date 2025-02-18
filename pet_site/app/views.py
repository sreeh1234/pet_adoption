from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
# import os
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import random

# Create your views here.

def pet_login(req):
    if 'shop' in req.session:
        return redirect(admin_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        shop=authenticate(username=uname,password=password)
        if shop:
            login(req,shop)
            if shop.is_superuser:
                
                req.session['shop']=uname       
                return redirect(admin_home)
            else:
                req.session['user']=uname
                return redirect(user_home)
        else:
            messages.warning(req,'invalid username or password')
            return redirect(pet_login)
    else:
        return render(req,'login.html')

def pet_logout(req):
    logout(req)
    req.session.flush()        
    return redirect(pet_login)


#-----------------------admin-----------------------


def admin_home(req):
    if 'shop' in req.session:
        # products=details.objects.all()
        return render(req,'admin/home.html')
    else:
        return redirect(pet_login)




#-----------------------user-----------------------

def register(req):
    if req.method == 'POST':
        uname = req.POST['uname']
        email = req.POST['email']
        pswd = req.POST['pswd']
        try:
            data = User.objects.create_user(first_name=uname, email=email, username=email, password=pswd)
            data.save()
            otp = ""
            for i in range(6):
                otp += str(random.randint(0, 9))
            msg = f'Your registration is completed otp: {otp}'
            otp = Otp.objects.create(user=data, otp=otp)
            otp.save()
            send_mail('Registration', msg, settings.EMAIL_HOST_USER, [email])
            messages.success(req, "Registration successful. Please check your email for OTP.")
            return redirect(otp_confirmation)
        except:
            messages.warning(req, 'Email already exists')
            return redirect(register)
    else:
        return render(req, 'user/register.html')

    
def otp_confirmation(req):
    if req.method == 'POST':
        uname = req.POST.get('uname')
        user_otp = req.POST.get('otp')
        try:
            user = User.objects.get(username=uname)
            generated_otp = Otp.objects.get(user=user)
    
            if generated_otp.otp == user_otp:
                generated_otp.delete()
                return redirect(pet_login)
            else:
                messages.warning(req, 'Invalid OTP')
                return redirect(otp_confirmation)
        except User.DoesNotExist:
            messages.warning(req, 'User does not exist')
            return redirect(otp_confirmation)
        except Otp.DoesNotExist:
            messages.warning(req, 'OTP not found or expired')
            return redirect(otp_confirmation)
    return render(req, 'user/otp.html')


def user_home(req):
    if 'user' in req.session:
        # products=product.objects.all()
        # data=category.objects.all()
        return render(req,'user/home.html')
    else:
        return redirect(pet_login)
    
def addpets(req):
    if 'user' in req.session:
        if req.method=='POST':
            pet_type=req.POST['p_type']
            pet_name=req.POST['p_name']
            pet_dis=req.POST['p_dis']
            pet_breed=req.POST['p_breed']
            pet_price=req.POST['p_price']
            pet_img=req.FILES['p_img']
            data=Pet.objects.create(p_name=pet_name,p_dis=pet_dis,p_breed=pet_breed,p_price=pet_price,p_img=pet_img,Pet_Type=PetType.objects.get(PetType=pet_type))
            data.save()
            return redirect(user_home)
        else:
            data=PetType.objects.all()
            return render(req,'user/addpets.html')  
    else:
        return redirect(pet_login)    