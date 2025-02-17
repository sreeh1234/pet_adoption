from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

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

# def register(req):
#     if req.method == 'POST':
#         uname = req.POST['uname']
#         email = req.POST['email']
#         pswd = req.POST['pswd']
#         try:
#             data = User.objects.create_user(first_name=uname, email=email, username=email, password=pswd)
#             data.save()
#             otp = ""
#             for i in range(6):
#                 otp += str(random.randint(0, 9))
#             msg = f'Your registration is completed otp: {otp}'
#             otp = Otp.objects.create(user=data, otp=otp)
#             otp.save()
#             send_mail('Registration', msg, settings.EMAIL_HOST_USER, [email])
#             messages.success(req, "Registration successful. Please check your email for OTP.")
#             return redirect(otp_confirmation)
#         except:
#             messages.warning(req, 'Email already exists')
#             return redirect(register)
#     else:
#         return render(req, 'user/register.html')


def user_home(req):
    if 'user' in req.session:
        # products=product.objects.all()
        # data=category.objects.all()
        return render(req,'user/home.html')
    else:
        return redirect(pet_login)