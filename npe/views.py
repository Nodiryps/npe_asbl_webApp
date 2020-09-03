from django.http import HttpResponse
from django.shortcuts import render


def home(req):
    return render(req, 'home.html')


def about(req):
    return render(req, 'about.html')


def donations(req):
    return render(req, 'donations.html')