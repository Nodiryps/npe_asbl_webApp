from django.contrib import admin
from django.urls import path
from . import views

app_name='demands'

urlpatterns = [
    path('', views.demandList, name="demandList"),
    path('newDemand/<uuid:dogId>/<int:userId>/<str:demandType>/', views.newDemand, name="newDemand"),
    path('acceptDemand/<int:demandId>/', views.acceptDemand, name="demandAccept"),
    path('deleteDemand/<int:demandId>/', views.deleteDemand, name="demandDelete"),
    path('getDemandNb/', views.getDemandNb, name="getDemandNb"),
    path('getHostDemandByDog/<uuid:idDog>/', views.getHostDemandByDog, name="getHostDemandByDog"),
]