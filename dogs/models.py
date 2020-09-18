from django.db import models
from django.utils.deconstruct import deconstructible
import uuid


@deconstructible
class Dog(models.Model):
    objects = models.Manager()
    FEMALE = 'F'
    MALE = 'M'
    OTHER_GENDER = 'other'
    SMALL_SIZED = 'small'
    MEDIUM_SIZED = 'medium'
    BIG_SIZED = 'big'
    SEX_CHOICES = [ (FEMALE, 'Femelle'), (MALE, 'Mâle'), (OTHER_GENDER, 'Autre') ]
    SIZE_CHOICES = [ (SMALL_SIZED, 'Petit.e'), (MEDIUM_SIZED, 'Moyen.ne'), (BIG_SIZED, 'Grand.e'), ]

    idDog = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    dogBreed = models.CharField(max_length=50)
    birthDate = models.DateField(null=True)
    arrivalDate = models.DateField()
    dogCoat = models.CharField(max_length=50)
    recognitionSigns = models.CharField(max_length=250)

    hostFamily = models.ForeignKey('accounts.User', related_name='hostedDog', on_delete=models.SET_NULL, null=True, blank=True, default='')
    owner = models.ForeignKey('accounts.User', related_name='adoptedDog', on_delete=models.SET_NULL, null=True, blank=True, default='')
    sponsor = models.ForeignKey('accounts.User', related_name='sponsoredDog', on_delete=models.SET_NULL, null=True, blank=True, default='')
    hosted = models.BooleanField(default=False)
    adopted = models.BooleanField(default=False)
    sponsored = models.BooleanField(default=False)
    chipId = models.CharField(max_length=5, unique=True)

    hasHostDemand = models.BooleanField(default=False)
    hasAdoptionDemand = models.BooleanField(default=False)

    story = models.TextField(default='', max_length=500)
    sex = models.CharField(max_length=7, choices=SEX_CHOICES, default=FEMALE, blank=False)
    size = models.CharField(max_length=8, choices=SIZE_CHOICES, default=SMALL_SIZED, blank=False)
    serology = models.BooleanField(null=True)
    rabiesVaccines = models.BooleanField(default=False)
    picture = models.ImageField(default='defaultDog.png', blank=True)



    def is_a_female(self):
        return self.sex == 'F'


    def is_a_male(self):
        return self.sex == 'M'


    def is_rabiesVaccine_done(self):
        return "Oui" if self.rabiesVaccines else "Non"


    def get_hostFamily_name(self):
        return self.hostFamily if self.hostFamily else 'Pas encore'


    def get_owner_name(self):
        return self.owner if self.owner else 'Pas encore'


    def get_sponsor_name(self):
        return self.sponsor if self.sponsor else 'Pas encore'


    def get_arrival_date(self):
        return self.arrivalDate.strftime('%d/%m/%Y')


    def get_birth_date(self):
        return self.arrivalDate.strftime('%d/%m/%Y')


    def get_name(self):
        return self.name.capitalize()


    def get_gender(self):
        if self.sex == 'F':
            return 'Femelle'
        elif self.sex == 'M':
            return 'Mâle'
        else:
            return 'Autre'


    def get_recognition_signs(self):
        return self.recognitionSigns.split(',', 5)


    def get_story(self):
        if len(self.story) > 300:
            return self.story[0:300] + ' ...'
        else:
            return self.story


    def get_serology(self):
        if self.serology == None:
            return "Non mentionné"
        elif self.serology:
            return 'Positif'
        else:
            return 'Négatif'


    def __str__(self):
        return self.name + ' - ' + str(self.chipId)


# American Hairless Terrier
# American Staffordshire Terrier
# American Water Spaniel
# Anatolian Shepherd Dog
# Australian Cattle Dog
# Australian Shepherd
# Australian Terrier
# Azawakh
# Barbet
# Basenji
# Basset Hound
# Beagle
# Bearded Collie
# Beauceron
# Bedlington Terrier
# Belgian Malinois
# Belgian Sheepdog
# Belgian Tervuren
# Bergamasco Sheepdog
# Berger Picard
# Bernese Mountain Dog
# Bichon Frise
# Black and Tan Coonhound
# Black Russian Terrier
# Bloodhound
# Bluetick Coonhound
# Boerboel
# Border Collie
# Border Terrier
# Borzoi
# Boston Terrier
# Bouvier des Flandres
# Boxer
# Boykin Spaniel
# Briard
# Brittany
# Brussels Griffon
# Bull Terrier
# Bulldog
# Bullmastiff
# Cairn Terrier
# Canaan Dog
# Cane Corso
# Cardigan Welsh Corgi
# Cavalier King Charles Spaniel
# Cesky Terrier
# Chesapeake Bay Retriever
# Chihuahua
# Chinese Crested
# Chinese Shar-Pei
# Chinook
# Chow Chow
# Cirneco dell’Etna
# Clumber Spaniel
# Cocker Spaniel
# Collie
# Coton de Tulear
# Curly-Coated Retriever
# Dachshund
# Dalmatian
# Dandie Dinmont Terrier
# Doberman Pinscher
# Dogo Argentino
# Dogue de Bordeaux
# English Cocker Spaniel
# English Foxhound
# English Setter
# English Springer Spaniel
# English Toy Spaniel
# Entlebucher Mountain Dog
# Field Spaniel
# Finnish Lapphund
# Finnish Spitz
# Flat-Coated Retriever
# French Bulldog
# German Pinscher
# German Shepherd Dog
# German Shorthaired Pointer
# German Wirehaired Pointer
# Giant Schnauzer
# Glen of Imaal Terrier
# Golden Retriever
# Gordon Setter
# Grand Basset Griffon Vendéen
# Great Dane
# Great Pyrenees
# Greater Swiss Mountain Dog
# Greyhound
# Harrier
# Havanese
# Ibizan Hound
# Icelandic Sheepdog
# Irish Red and White Setter
# Irish Setter
# Irish Terrier
# Irish Water Spaniel
# Irish Wolfhound
# Italian Greyhound
# Japanese Chin
# Keeshond
# Kerry Blue Terrier
# Komondor
# Kuvasz
# Labrador Retriever
# Lagotto Romagnolo
# Lakeland Terrier
# Leonberger
# Lhasa Apso
# Löwchen
# Maltese
# Manchester Terrier (Standard)
# Manchester Terrier (Toy)
# Mastiff
# Miniature American Shepherd
# Miniature Bull Terrier
# Miniature Pinscher
# Miniature Schnauzer
# Neapolitan Mastiff
# Nederlandse Kooikerhondje
# Newfoundland
# Norfolk Terrier
# Norwegian Buhund
# Norwegian Elkhound
# Norwegian Lundehund
# Norwich Terrier
# Nova Scotia Duck Tolling Retriever
# Old English Sheepdog
# Otterhound
# Papillon
# Parson Russell Terrier
# Pekingese
# Pembroke Welsh Corgi
# Petit Basset Griffon Vendéen
# Pharaoh Hound
# Plott Hound
# Pointer
# Polish Lowland Sheepdog
# Pomeranian
# Poodle (Miniature)
# Poodle (Standard)
# Poodle (Toy)
# Portuguese Podengo Pequeno
# Portuguese Water Dog
# Pug
# Puli
# Pumi
# Pyrenean Shepherd
# Rat Terrier
# Redbone Coonhound
# Rhodesian Ridgeback
# Rottweiler
# Russell Terrier
# Saint Bernard
# Saluki
# Samoyed
# Schipperke
# Scottish Deerhound
# Scottish Terrier
# Sealyham Terrier
# Shetland Sheepdog
# Shiba Inu
# Shih Tzu
# Siberian Husky
# Silky Terrier
# Skye Terrier
# Sloughi
# Smooth Fox Terrier
# Soft Coated Wheaten Terrier
# Spanish Water Dog
# Spinone Italiano
# Staffordshire Bull Terrier
# Standard Schnauzer
# Sussex Spaniel
# Swedish Vallhund
# Tibetan Mastiff
# Tibetan Spaniel
# Tibetan Terrier
# Toy Fox Terrier
# Treeing Walker Coonhound
# Vizsla
# Weimaraner
# Welsh Springer Spaniel
# Welsh Terrier
# West Highland White Terrier
# Whippet
# Wire Fox Terrier
# Wirehaired Pointing Griffon
# Wirehaired Vizsla
# Xoloitzcuintli
# Yorkshire Terrier