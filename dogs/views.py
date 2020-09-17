from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .models import Dog
from accounts.models import User
from .forms import DogCreationForm, DogUpdateForm


def dogList(req):
    dogs = Dog.objects.filter(adopted=False).order_by('arrivalDate')
    template = 'dogs/dogList.html'
    templateAjax = 'dogs/dogListCards.html'

    if not req.user and not req.user.is_admin:
        dogs = [dog for dog in dogs if dog.hasAdoptionDemand == False]

    if req.method == 'GET':
        if req.GET.get('query'):
            dogs = search(req, dogs)
        if req.GET.get('genderFilter'):
            dogs = genderFilter(req, dogs)

    if req.is_ajax():
        return ajaxRender(req, templateAjax, {'dogs': dogs, 'currUser': req.user})
    else:
        return render(req, template, {
            'dogs': dogs,
            'currUser': req.user,
            'isDogContent': True
        })


def ajaxRender(req, template, contxt):
    html = render_to_string(
        template_name=template,
        context=contxt
    )
    data_dict = {'html_from_view': html}

    return JsonResponse(data=data_dict, safe=False)


def genderFilter(req, dogs):
    gender = req.GET.get('genderFilter')

    if gender != 'all':
            dogs = dogs.filter(sex=gender).order_by('arrivalDate')

    return dogs


def search(req, dogs):
    query = req.GET.get('query')

    if query:
        dogs = dogs.filter(name__icontains=query) #i: not case sensitive

#       if not dogs.exists():
#            dogs = dogs.filter(dogBreed__icontains=query)
        if not dogs.exists():
            dogs = searchAdmin(req, dogs, query)

    return dogs


@login_required
def searchAdmin(req, dogs, query):
    if req.user.is_admin:
        dogs = dogs.filter(chipId__contains=query)
    return dogs


def dogDetails(req, dogId):
    if req.is_ajax():
        dog = Dog.objects.filter(idDog=dogId)
        serialized = serializers.serialize('json', dog)
        return JsonResponse(serialized, safe=False)
    else:
        dog = Dog.objects.get(idDog=dogId)
        return render(req, 'dogs/dogDetails.html', {
            'dog': dog,
            'currUser': req.user,
            'isDogContent': True
        })


@login_required
def createDog(req):
    if req.user.is_admin:
        if req.method == 'POST':
            form = DogCreationForm(req.POST, req.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = DogCreationForm()
        return render(req, 'dogs/dogCreation.html', {
            'isDogContent': True,
            'dog': None,
            'form': form,
        })


@login_required
def updateDog(req, dogId):
    if req.user.is_admin:
        dog = Dog.objects.get(idDog=dogId)
        if req.method == 'POST':
            setHostedAdoptedOrSponsored(dog)
            form = DogUpdateForm(req.POST, req.FILES, instance=dog)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = DogUpdateForm(instance=dog)

        return render(req, 'dogs/dogUpdate.html', {
            'dog': dog,
            'form': form,
        })


def setHostedAdoptedOrSponsored(dog):
    if dog.hostFamily:
        dog.hosted = True
    elif dog.owner:
        dog.adopted = True
    elif dog.sponsor:
        dog.sponsored = True


@login_required
def deleteDog(req, dogId):
    if req.user.is_admin:
        dog = Dog.objects.get(idDog=dogId)
        if req.method == 'POST':
            dog.delete()
            return redirect('home')
        return render(req, 'dogs/dogDelete.html', {
            'dog': dog,
        })


@login_required
def sponsorDog(req, dogId, userId):
    dog = Dog.objects.get(idDog=dogId)
    user = User.objects.get(id=userId)

    if req.is_ajax():
        dog.sponsor = user
        dog.sponsored = True
        dog.save()

    return ajaxRender(req, 'dogs/dogDetails.html', {'dog': dog})


# def error_404(req, exc):
#     data = {}
#     return render(req, 'dogs/404.html', data)


# def error_500(req):
#     data = {}
#     return render(req, 'dogs/500.html', data)