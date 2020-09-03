from django.contrib import admin
from django.urls import path
from . import views

app_name='posts'

urlpatterns = [
    path('', views.postList, name="postList"),
    # path('createPost/<str:dog>/<str:body>/<str:pict>/', views.createPost, name="createPost"),
    path('postCreation/', views.createPost, name="postCreation"),
]