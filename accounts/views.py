from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
from .forms import MyUserCreationForm, MyUserUpdateForm
from .models import User
from demands.models import Demand
from dogs.models import Dog
import re


def signupView(req):
    if req.method == 'POST':
        form = MyUserCreationForm(req.POST)
        if form.is_valid():
            if form.cleaned_data['username'] == '':
                user = form.save(commit=False)
                user.username = generateUsername(
                        user.firstName,
                        user.lastName,
                        user.birthDate
                    )
                user.save()
                form.save_m2m()
            else:
                user = form.save()
            login(req, user)
            return redirect('home')
    else:
        form = MyUserCreationForm()
    return render(req, 'accounts/signup.html', {'form': form,})


def loginView(req):
    if req.method == 'POST':
        form = AuthenticationForm(data=req.POST)
        if form.is_valid():
            user = form.get_user()
            login(req, user)
            route = 'home'
            if 'next' in req.POST:
                route = req.POST.get('next')
            return redirect(route)
    else:
        form = AuthenticationForm()
    return render(req, 'accounts/login.html', {'form': form,})


@login_required
def logoutView(req):
    if req.user:
        if req.method == 'POST':
            logout(req)
    return redirect('home')


@login_required
def userProfile(req):
    return render(req, 'accounts/userProfile.html', {
        'currUser': req.user,
        'demands': getUserDemands(req),
        'dogs': getUserDogs(req),
    })


@login_required
def getUserDogs(req):
    user = User.objects.get(id=req.user.id)
    dogs = Dog.objects.filter(owner=user) | Dog.objects.filter(hostFamily=user) | Dog.objects.filter(sponsor=user)
    return dogs


@login_required
def getUserDemands(req):
    user = User.objects.get(id=req.user.id)
    demands = Demand.objects.filter(applicant=user)
    if req.is_ajax():
        serialized = serializers.serialize('json', demands)
        return JsonResponse(serialized, safe=False)
    else:
        return demands


@login_required
def updateDogName(req, dogId, newName):
    dog = Dog.objects.get(idDog=dogId)
    if dog:
        dog.name = newName
        dog.save()

    if req.is_ajax():
        return ajaxRender(req, 'accounts/userProfile.html', {
            'currUser': req.user,
            'demands': getUserDemands(req),
            'dogs': getUserDogs(req),
        })
    else:
        return userProfile()


def ajaxRender(req, template, contxt):
    html = render_to_string(
        template_name=template,
        context=contxt
    )
    data_dict = {'html_from_view': html}

    return JsonResponse(data=data_dict, safe=False)


@login_required
def userList(req):
    if req.user.is_admin:
        users = User.objects.all().order_by('username')
        return render(req, 'accounts/userList.html', {
            'users': users,
            'currUser': req.user,
            'isDogContent': False
        })


def replaceSpecialCharsUsername(string):
    string = string.replace(" ", '')
    string = string.replace("\'", '')
    string = string.replace("´", '')
    string = string.replace("-", '')
    return string


def usernameUniqueness(username):
    pattern = re.compile("^[0-9]*$")
    lastChar = username[len(username) -1]

    if pattern.search(lastChar):
        username = username[:len(username) -1] + str(int(lastChar) + 1)
    else:
        username = username + "1"

    return username


def generateUsername(fname, lname, bdate):
    bdatePart = "".join([bdate.strftime("%d"), bdate.strftime("%m")])

    fname = replaceSpecialCharsUsername(fname)
    lname = replaceSpecialCharsUsername(lname)

    namePart = "".join([fname[:2].lower(), lname.lower()])

    username = "{}{}".format(bdatePart, namePart)

    if isUsernameUnique(username):
        return username
    else:
        return usernameUniqueness(username)


@login_required
def createUser(req):
    if req.user.is_admin:
        if req.method == 'POST':
            form = MyUserCreationForm(req.POST)
            if form.is_valid():
                if form.cleaned_data['username'] == '':
                    user = form.save(commit=False)
                    user.username = generateUsername(
                            user.firstName,
                            user.lastName,
                            user.birthDate
                        )
                    user.save()
                    form.save_m2m()
                else:
                    form.save()
                return redirect('accounts:userList')
        else:
            form = MyUserCreationForm()
        return render(req, 'accounts/userCreation.html', {
            'user': None,
            'form': form,
        })
    else:
        return redirect('accounts:userList')


@login_required
def updateUser(req, userId):
    if req.user.id == userId:
        user = User.objects.get(id=userId)
        if req.method == 'POST':
            form = MyUserUpdateForm(req.POST, req.FILES, instance=user)
            if form.is_valid():
                form.save()
                return redirect('accounts:userList')
        else:
            form = MyUserUpdateForm(instance=user)

        return render(req, 'accounts/userUpdate.html', {
            'user': user,
            'currUser': req.user,
            'form': form
        })
    else:
        return redirect('accounts:userList')


@login_required
def deleteUser(req, userId):
    if req.user.is_admin & req.user.id != userId:
        user = User.objects.get(id=userId)
        if req.method == 'POST':
            user.delete()
            return redirect('accounts:userList')
        return render(req, 'accounts/userDelete.html', {
            'user': user,
        })
    else:
        return redirect('accounts:userList')


@login_required
def userDetails(req, userId):
    if req.user.is_admin:
        user = User.objects.filter(id=userId)
        serialized = serializers.serialize('json', user)
        return JsonResponse(serialized, safe=False)
        # return HttpResponse(serialized)


def isUsernameUnique (username):
    if username:
        query = User.objects.filter(username=username).count()
        return query == 0


def isEmailUnique (req):
    email = req.GET.get('email', False)

    if email:
        query = User.objects.filter(email=email).count()
        return foundInDataBase(query)


def isPhoneNumberUnique (req):
    phoneNumber = req.GET.get('phoneNumber', False)

    if phoneNumber:
        query = User.objects.filter(phoneNumber=phoneNumber).count()
        return foundInDataBase(query)


def isNationalNumberUnique (req):
    nationalNumber = req.GET.get('nationalNumber', False)

    if nationalNumber:
        query = User.objects.filter(nationalNumber=nationalNumber).count()
        return foundInDataBase(query)


def foundInDataBase (query):
    if query == 0:
        return HttpResponse('true')
    else:
        return HttpResponse('false')