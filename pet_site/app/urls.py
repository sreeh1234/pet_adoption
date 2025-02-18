from django .urls import path 
from . import views 


urlpatterns=[

    path('',views.pet_login),
    path('logout',views.pet_logout),

#--------------------admin----------------------------

    path('admin_home',views.admin_home),


#--------------------user-----------------------------

    path('register',views.register),
    path('otp',views.otp_confirmation),
    path('user_home',views.user_home),
    path('add_pets',views.addpets),
    



]    