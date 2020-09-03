from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import json
import ast


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Email requis")
        if not username:
            raise ValueError("Pseudo requis")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_superuser'):
            raise ValueError('Super User must have is_superuser to True!')

        user = self.create_user(
            # email=self.normalize_email(email),
            username=username,
            password=password,
            **extra_fields
        )

        # user.is_admin = True
        # user.is_staff = True
        # user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    def get_localities_and_postal_codes(keyOrValueStr): # key == loc & value == pCode
        path = '{}/{}'.format(settings.STATICFILES_DIRS[0], 'localitiesAndPostalCodes.txt')
        with open(path) as myFile:
            dataRaw = myFile.read()
            locAndPostCodesDict = ast.literal_eval(dataRaw)
            choices = []

            if locAndPostCodesDict:
                if keyOrValueStr == 'keys':
                    kovDict = locAndPostCodesDict.keys()
                elif keyOrValueStr == 'values':
                    kovDict = locAndPostCodesDict.values()

                for kov in kovDict:
                    choices.append((kov, kov.lower()))

            choices.sort()

        return tuple(choices)


    objects = UserManager()
    UNICITY_MSG = _("Déjà pris, pas assez rapide ;)")


    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='date de création', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='date dernière connexion', auto_now=True)

    isOwner = models.BooleanField(default=False)
    isHost = models.BooleanField(default=False)
    isSponsor = models.BooleanField(default=False)
    lastName = models.CharField(max_length=60)
    firstName = models.CharField(max_length=60)
    birthDate = models.DateField(null=True)
    nationalNumber = models.CharField(max_length=20, unique=True, error_messages={'unique': UNICITY_MSG})
    email = models.EmailField(max_length=60, unique=True, error_messages={'unique': UNICITY_MSG})
    phoneNumber = models.CharField(max_length=13, unique=True, error_messages={'unique': UNICITY_MSG})
    streetName = models.CharField(max_length=100)
    streetNumber = models.CharField(max_length=4)
    postalCode = models.CharField(max_length=4, choices=get_localities_and_postal_codes('values'))
    town = models.CharField(max_length=60, choices=get_localities_and_postal_codes('keys'))
    username = models.CharField(max_length=30, blank=True, unique=True, error_messages={'unique': UNICITY_MSG}) # blank if js is down
    password = models.CharField(max_length=100)
    # favoriteDogsList
    # photo + ID picture

    USERNAME_FIELD = 'username' # to change username to email, to log in
    REQUIRED_FIELDS = ['email',]


    def __str__(self):
        return self.username


    def get_full_name(self):
        fullname = '%s %s' % (self.firstName, self.lastName)
        return fullname.strip()


    def get_full_address(self):
        address = '{} {}, {} {}'.format(self.streetNumber, self.streetName, self.postalCode, self.town)
        return address


    def send_email(self, subject, msg, from_email=None, **kwargs):
        send_mail(subject, msg, from_email, [self.email], **kwargs)


    def has_perm(self, perm, obj=None):
        return self.is_active


    def has_module_perms(self, app_label):
        return True