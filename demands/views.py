from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from accounts.models import User
from dogs.models import Dog
from .models import Demand


@login_required
def demandList(req):
    if req.user.is_admin:
        demands = Demand.objects.all().order_by('demandType')
        return render(req, 'demands/demandList.html', {
            'demands': demands,
            'currUser': req.user,
        })
    else:
        return redirect('home')


@login_required
def newDemand(req, dogId, userId, demandType):
    dog = Dog.objects.get(idDog=dogId)
    user = User.objects.get(id=userId)

    if req.method == 'POST' and isDogAvailableForNewDemand(dog, demandType):
        demand = Demand(dog=dog, applicant=user, demandType=demandType)
        setHasDemandBool(demand.dog, demandType, True)
        demand.save()
        print('NEW_DEMAND:', demand.applicant)
        return redirect('home')


def isDogAvailableForNewDemand(dog, demandType):
    boolean = False

    if not dog.adopted:
        if not dog.hosted and demandType == 'hosting':
            if not dog.hasAdoptionDemand and not dog.hasHostDemand:
                boolean = True
        elif demandType == 'adoption' and not dog.hasAdoptionDemand:
            boolean = True

    return boolean


def setHasDemandBool(dog, demandType, val):
    if demandType == 'adoption':
        dog.hasAdoptionDemand = val
        dog.save()
    elif demandType == 'hosting':
        dog.hasHostDemand = val
        dog.save()


@login_required
def acceptDemand(req, demandId):
    demand = Demand.objects.get(id=demandId)
    user = User.objects.get(id=demand.applicant.id)
    if req.user.is_admin and not req.user == user:
        if req.method == 'POST':
            demandType = demand.demandType
            dog = Dog.objects.get(idDog=demand.dog.idDog)
            print('ACCEPT_DEMAND:', user)

            updateAcceptedDemandDog(demand, demandType, dog, user)
            deleteAcceptedDemand(demand, demandType, dog)

            return redirect('demands:demandList')

        return render(req, 'demands:demandList')


def updateAcceptedDemandDog(demand, demandType, dog, user):
    if demandType == 'adoption':
        dog.owner = user
        dog.hostFamily = None
        dog.sponsor = None
        dog.adopted = True
        dog.hosted = False
        dog.sponsored = False
        setHasDemandBool(dog, demandType, False)
        setHasDemandBool(dog, 'hosting', False)
        dog.save()

        user.isOwner = True
        user.save()

    elif demandType == 'hosting':
        dog.hostFamily = user
        dog.hosted = True
        setHasDemandBool(dog, demandType, False)
        dog.save()

        user.isHost = True
        user.save()


def deleteAcceptedDemand(demand, demandType, dog):
    demand.delete()
    # if host dem on same dog while adopt° accepted
    if demandType == 'adoption':
        hostDem = Demand.objects.filter(dog=dog)
        if hostDem:
            hostDem.delete()


@login_required
def deleteDemand(req, demandId):
    demand = Demand.objects.get(id=demandId)
    if demand.applicant == req.user or req.user.is_admin:
        if req.method == 'POST':
            setHasDemandBool(demand.dog, demand.demandType, False)
            demand.delete()
            return redirect('demands:demandList')
        return render(req, 'demands/demandList.html')


@login_required
def getDemandNb(req):
    return JsonResponse(Demand.objects.count(), safe=False)


@login_required
def getHostDemandByDog(req, idDog):
    if req.user.is_admin:
        if req.is_ajax():
            dog = Dog.objects.get(idDog=idDog)
            demands = Demand.objects.filter(dog=dog)
            if dog.hasHostDemand and not dog.hosted:
                demand = demands.get(demandType='hosting')
                return JsonResponse(demand.id, safe=False)
            else:
                return JsonResponse('', safe=False)
