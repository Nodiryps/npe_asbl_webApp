from django.contrib import admin
from django.urls import path
from . import views

app_name='dogs'

urlpatterns = [
    path('', views.dogList, name="dogList"),
    path('<uuid:dogId>/', views.dogDetails, name="dogDetails"),
    path('dogDetails/<uuid:dogId>/', views.dogDetails, name="dogDetails"),
    path('dogCreation/', views.createDog, name="dogCreation"),
    path('dogUpdate/<uuid:dogId>/', views.updateDog, name="dogUpdate"),
    path('dogDelete/<uuid:dogId>/', views.deleteDog, name="dogDelete"),
    path('sponsorDog/<uuid:dogId>/<int:userId>/', views.sponsorDog, name="sponsorDog"),
    # path('search/<str:dog>', views.search, name="dogSearch"),
]

# handler500 = 'dogs.views.error_500'
# handler404 = 'dogs.views.error_404'
# handler403 = 'dogs.views.error_403'
# handler400 = 'dogs.views.error_400'