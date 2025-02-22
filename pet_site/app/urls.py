from django .urls import path 
from . import views 


urlpatterns=[

    path('',views.pet_login),
    path('logout',views.pet_logout),

#--------------------admin----------------------------

    path('admin_home',views.admin_home),
    path('cat',views.cat),

#--------------------user-----------------------------

    path('register',views.register),
    path('otp',views.otp_confirmation),
    path('user_home',views.user_home),
    path('add-pet', views.add_pet, name='add_pet'),
    path('add-category', views.add_category, name='add_category'),
    path('add-pet-type', views.add_pet_type, name='add_pet_type'),
    path('pet-list', views.pet_list, name='pet_list'),
    path('pet-detail/<int:pet_id>', views.pet_detail, name='pet_detail'),
    path('pet/edit/<int:pet_id>', views.edit_pet, name='edit_pet'),
    path('pet/<int:id>/delete/', views.delete_pet, name='delete_pet'),
    



]    