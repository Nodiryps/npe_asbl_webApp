from django.contrib import admin
from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('signup/', views.signupView, name="signup"),
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('', views.userList, name="userList"),
    path('userProfile/', views.userProfile, name="userProfile"),
    path('userProfile/updateDogName/<uuid:dogId>/<str:newName>/', views.updateDogName, name="updateDogName"),
    path('getUserDemands/<int:userId>/', views.getUserDemands, name="getUserDemands"),
    path('userCreation/', views.createUser, name="userCreation"),
    path('userDetails/<int:userId>/', views.userDetails, name="userDetails"),
    path('userUpdate/<int:userId>/', views.updateUser, name="userUpdate"),
    path('userDelete/<int:userId>/', views.deleteUser, name="userDelete"),
    path('isUsernameUnique/', views.isUsernameUnique, name="isUsernameUnique"),
    path('isEmailUnique/', views.isEmailUnique, name="isEmailUnique"),
    path('isPhoneNumberUnique/', views.isPhoneNumberUnique, name="isPhoneNumberUnique"),
    path('isNationalNumberUnique/', views.isNationalNumberUnique, name="isNationalNumberUnique"),
]