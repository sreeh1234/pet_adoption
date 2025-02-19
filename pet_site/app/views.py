from django.shortcuts import render,redirect, get_object_or_404
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
    
def cat(req):
    if req.method=="POST":
        categories=req.POST['category']
        data=Category.objects.create(categories=categories)
        data.save()
        return redirect(cat)
    else:
        data=Category.objects.all()
        return render(req,'admin/category.html',{'data':data})     




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
    


def add_pet(request):
    categories = Category.objects.all()
    pet_types = PetType.objects.all()

    if request.method == 'POST':
        pet_name = request.POST.get('pet_name')
        pet_description = request.POST.get('pet_description')
        pet_age = request.POST.get('pet_age')
        pet_price = request.POST.get('pet_price')
        pet_breed = request.POST.get('pet_breed')
        category_id = request.POST.get('category')
        pet_type_id = request.POST.get('pet_type')
        pet_image = request.FILES.get('pet_image')  
        category = Category.objects.get(id=category_id)
        pet_type = PetType.objects.get(id=pet_type_id)
        
        pet = Pet(
            pet_name=pet_name,
            pet_description=pet_description,
            pet_age=pet_age,
            pet_price=pet_price,
            pet_breed=pet_breed,
            category=category,
            pet_type=pet_type,
            pet_image=pet_image
        )
        pet.save()


        return redirect('pet_list') 

    
    return render(request, 'user/addpets.html', {'categories': categories, 'pet_types': pet_types})
  






def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('name')
        category = Category(name=category_name)
        category.save()
        
        
        messages.success(request, 'Category added successfully!')
        return redirect('add_category')  

    return render(request, 'user/add_category.html')


def add_pet_type(request):
    if request.method == 'POST':
        pet_type_name = request.POST.get('name')
        
        pet_type = PetType(name=pet_type_name)
        pet_type.save()
        
        messages.success(request, 'Pet type added successfully!')
        return redirect('add_pet_type')  

    return render(request, 'user/add_pet_type.html')

def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'user/pet_detail.html', {'pet': pet})

def pet_list(request):
    pets = Pet.objects.all()[::-1]
    return render(request, 'user/pet_list.html', {'pets': pets})




# def edit_pet(request, id):
#     pet = get_object_or_404(Pet, id=id)

#     if request.method == 'POST':
#         pet.pet_name = request.POST.get('pet_name', pet.pet_name)
#         pet.pet_description = request.POST.get('pet_description', pet.pet_description)
#         pet.pet_age = request.POST.get('pet_age', pet.pet_age)
#         pet.pet_breed = request.POST.get('pet_breed', pet.pet_breed)
#         pet.pet_price = request.POST.get('pet_price', pet.pet_price)
#         pet.category = request.POST.get('category', pet.category)

#         # Handling file input (image)
#         if request.FILES.get('pet_image'):
#             pet.pet_image = request.FILES['pet_image']

#         # Handling pet_type assignment with error checking
#         pet_type_name = request.POST.get('pet_type')
#         try:
#             pet_type_instance = PetType.objects.get(name=pet_type_name)
#             pet.pet_type = pet_type_instance
#         except PetType.DoesNotExist:
#             # Handle the case where pet_type doesn't exist
#             return render(request, 'user/edit_pet.html', {'pet': pet, 'error': 'Invalid pet type selected.'})

#         pet.save()  # Save the updated pet object
#         return redirect('pet_detail', id=pet.id)

#     return render(request, 'user/edit_pet.html', {'pet': pet})



def delete_pet(request, id):
    pet = get_object_or_404(Pet, id=id)

    if request.method == 'POST':
        pet.delete()
        return redirect('pet_list')

    return render(request, 'confirm_delete.html', {'pet': pet})

