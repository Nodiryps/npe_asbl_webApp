# from django.forms import ModelForm
from django import forms
from datetime import date, datetime
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import re
import ast
from .models import User


class MyUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Mot de passe'
    )
    passwordConf = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirmation du mdp'
    )
    birthDate = forms.DateField(
        # input_formats=['%d/%m/%Y', ],
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(
            attrs={
                'placeholder': 'jj/mm/aaaa',
                # 'type': 'date',
                # 'value': datetime.now().strftime('%d/%m/%Y')
            })
    )

    class Meta:
        model = User
        fields = '__all__'
        exclude = (
            'is_admin',
            'is_active',
            'is_staff',
            'is_superuser',
            'isOwner',
            'isHost',
            'isSponsor',
        )

        labels = {
            'lastName':         _('Nom'),
            'firstName':        _('Prénom'),
            'birthDate':        _('Date de naissance'),
            'email':            _('Email'),
            'phoneNumber':      _('Téléphone'),
            'streetNumber':     _('Numéro'),
            'streetName':       _('Rue'),
            'town':             _('Ville'),
            'postalCode':       _('Code postale'),
            'nationalNumber':   _('Numéro national'),
            'username':         _(''),
            'password':         _('Mot de passe'),
        }

        widgets = {
            'username': forms.HiddenInput(),
            'nationalNumber': forms.TextInput(attrs={'placeholder': 'xx.xx.xx-xxx.xx'}),
            'phoneNumber': forms.TextInput(attrs={'placeholder': 'ex.: 0498 12 34 56'}),
            'password': forms.TextInput(attrs={'placeholder': 'min. 20 caractères'}),
        }

        error_messages = {
            'lastName':         {'required': _("Champ requis")},
            'firstName':        {'required': _("Champ requis")},
            'birthDate':        {'required': _("Champ requis")},
            'email':            {'required': _("Champ requis")},
            'phoneNumber':      {'required': _("Champ requis")},
            'streetName':       {'required': _("Champ requis")},
            'streetNumber':     {'required': _("Champ requis")},
            'postalCode':       {'required': _("Champ requis")},
            'town':             {'required': _("Champ requis")},
            'nationalNumber':   {'required': _("Champ requis")},
            'password':         {'required': _("Champ requis")},
            'passwordConf':     {'required': _("Champ requis")},
        }


    MIN_AGE_TO_SUB = 18
    MIN_LENGTH_USERNAME = 5
    MAX_LENGTH_USERNAME = 30
    MIN_LENGTH_STREET_NUMBER = 1
    MAX_LENGTH_STREET_NUMBER = 4
    POSTAL_CODE = 4
    MIN_LENGTH_PASSWORD = 5
    MAX_LENGTH_PASSWORD = 100
    MIN_LENGTH_STREET_NAME = 9
    MIN_LENGTH_NAMES = 2
    MAX_LENGTH_NAMES = 60
    MOBILE_NUM_LENGTH = 10
    LAND_LINE_NUM_LENGTH = 9

    MAY_ONLY_CONTAINS = "Ne peut contenir que "
    DIGITS_MSG = MAY_ONLY_CONTAINS + "des chiffres "
    CHARS_MSG = MAY_ONLY_CONTAINS + "des lettres "
    SPECIAL_CHARS_MSG = "certains caractères spéciaux "
    INVALID_FORMAT_MSG = "Format invalide "
    REQUIRED_MSG = _("Champ requis")
    DIGITS_AND_PUNCT_MSG = _(DIGITS_MSG + "et " + SPECIAL_CHARS_MSG)
    CHARS_AND_PUNCT_MSG = _(CHARS_MSG + "et " + SPECIAL_CHARS_MSG)
    CHARS_PUNCT_AND_NUMBERS_MSG = _(DIGITS_MSG + " des lettres et " + SPECIAL_CHARS_MSG)
    PHONE_NUMBER_FORMAT_MSG = _("Format du numéro invalide")
    PHONE_NUMBER_MSG = _(DIGITS_MSG + "et doit commencer par un \"zéro\" (0)")
    BIRTH_DATE_MSG = _(INVALID_FORMAT_MSG + "(ex.: 01/12/1990)")
    MIN_AGE_TO_SUB_MSG = _("Il faut, au moins, avoir 18 ans")
    NAT_NUM_COMPARED_TO_B_DATE_MSG = _("La date de naissance et le numéro national ne correspondent pas")
    NATIONAL_NUMBER_MSG = _(INVALID_FORMAT_MSG + "(ex.: 90.12.01-123.45)")
    LOCALITY_COMPARED_TO_P_CODE_MSG = _("La ville et le code postal ne correspondent pas")
    PASSWORD_CONF_NOT_EQUAL_MSG = _("Les mots de passe doivent être identiques")
    PASSWORD_SPECS_MSG = _(DIGITS_MSG + "des lettres et " + SPECIAL_CHARS_MSG)


    @staticmethod
    def errorMsgMaxLength(maxlength):
        return _(f"Trop long, allez-y doucement :) (max. {maxlength})")


    @staticmethod
    def errorMsgMinLength(minlength):
        return _(f"Trop court, encore un petit effort :) (min. {minlength})")


    @staticmethod # implicit first arg --> def fct(self, arg)
    def checksPhoneNumberPattern(string):
        pattern = re.compile("^[0]+[0-9]+(?:[ ][0-9]+)*$")
        return pattern.search(string)


    @staticmethod
    def checksNamePattern(string):
        # pattern = re.compile("^[A-Za-z]+(?:[ '-][A-Za-zéèëêîïàç]+)*$")
        pattern = re.compile("^[^0-9_!¡?÷?¿/\\+=*@#$€@µ%&^°§²³`(){\}|~<>;,:\[\]]*$")
        return pattern.search(string)


    @staticmethod
    def checksDigitsOnlyPattern(string):
        pattern = re.compile("^[0-9]*$")
        return pattern.search(string)


    @staticmethod
    def checksNatNumPattern(string):
        pattern = re.compile("^[0-9]{2}.[0-9]{2}.[0-9]{2}-[0-9]{3}.[0-9]{2}$")
        return pattern.search(string)


    @staticmethod
    def checksBirthDatePattern(bdate):
        bdateStr = "/".join([bdate.strftime("%d"), bdate.strftime("%m"),bdate.strftime("%Y")])

        return bdateStr == datetime.strptime(bdateStr, "%d/%m/%Y").strftime("%d/%m/%Y")


    @staticmethod
    def checksPasswordPattern(string):
        pattern = re.compile("^[A-Za-z0-9]+(?:[ '=*/+-.,;:/µ£_!?~%&§°]+)*$")
        return pattern.search(string)


    def lengthValidation(self, string, minVal, maxVal):
        if len(string) < minVal:
            raise forms.ValidationError(self.errorMsgMinLength(minVal))

        if len(string) > maxVal:
            raise forms.ValidationError(self.errorMsgMaxLength(maxVal))


    def nameSpecsValidation(self, string):
        if not self.checksNamePattern(string):
            raise forms.ValidationError(self.CHARS_AND_PUNCT_MSG)

        self.lengthValidation(string, self.MIN_LENGTH_NAMES, self.MAX_LENGTH_NAMES)


    def getAge(self, bdate):
        today = date.today()
        years = today.year - bdate.year
        return years - ((today.month, today.day) < (bdate.month, bdate.day))


    def birthDateSpecsValidation(self, string):
        if not self.checksBirthDatePattern(string):
            raise forms.ValidationError(self.BIRTH_DATE_MSG)

        if self.getAge(string) < self.MIN_AGE_TO_SUB:
            raise forms.ValidationError(self.MIN_AGE_TO_SUB_MSG)


    def nationalNumberSpecsValidation(self, string):
        if not self.checksNatNumPattern(string):
            raise forms.ValidationError(self.NATIONAL_NUMBER_MSG)


    def isMobileNumber(self, string):
        string = string.replace(" ", "")
        twoFirst = string[:2]
        return len(string) == self.MOBILE_NUM_LENGTH and twoFirst == '04'


    def isLandlineNumber(self, string):
        string = string.replace(" ", "")
        return len(string) == self.LAND_LINE_NUM_LENGTH


    def phoneNumberSpecsValidation(self, string):
        if not self.checksPhoneNumberPattern(string):
            raise forms.ValidationError(self.PHONE_NUMBER_MSG)

        if not self.isLandlineNumber(string):
            if not self.isMobileNumber(string):
                raise forms.ValidationError(self.PHONE_NUMBER_FORMAT_MSG)


    def streetNameSpecsValidation(self, string):
        if not self.checksNamePattern(string):
            raise forms.ValidationError(self.CHARS_AND_PUNCT_MSG)

        self.lengthValidation(string, self.MIN_LENGTH_STREET_NAME, self.MAX_LENGTH_NAMES)


    def streetNumberSpecsValidation(self, string):
        if not self.checksDigitsOnlyPattern(string):
            raise forms.ValidationError(self.DIGITS_MSG)

        self.lengthValidation(string, self.MIN_LENGTH_STREET_NUMBER, self.MAX_LENGTH_STREET_NUMBER)


    def passwordSpecsValidation(self, string):
        if not self.checksPasswordPattern(string):
            raise forms.ValidationError(self.PASSWORD_SPECS_MSG)

        self.lengthValidation(string, self.MIN_LENGTH_PASSWORD, self.MAX_LENGTH_PASSWORD)


    def clean_lastName(self):
        lastName = self.cleaned_data['lastName']
        self.nameSpecsValidation(lastName)
        return lastName


    def clean_firstName(self):
        firstName = self.cleaned_data['firstName']
        self.nameSpecsValidation(firstName)
        return firstName


    def clean_birthDate(self):
        birthDate = self.cleaned_data['birthDate']
        self.birthDateSpecsValidation(birthDate)
        return birthDate


    def clean_nationalNumber(self):
        natNum = self.cleaned_data['nationalNumber']
        self.nationalNumberSpecsValidation(natNum)
        return natNum


    def clean_phoneNumber(self):
        phoneNumber = self.cleaned_data['phoneNumber']
        self.phoneNumberSpecsValidation(phoneNumber)
        return phoneNumber


    def clean_streetName(self):
        streetName = self.cleaned_data['streetName']
        self.streetNameSpecsValidation(streetName)
        return streetName


    def clean_streetNumber(self):
        streetNumber = self.cleaned_data['streetNumber']
        self.streetNumberSpecsValidation(streetNumber)
        return streetNumber


    def clean_town(self):
        town = self.cleaned_data['town']
        self.nameSpecsValidation(town)
        return town


    def clean_password(self):
        password = self.cleaned_data['password']
        self.passwordSpecsValidation(password)
        return password


    def passwordEqualsPasswordConf(self, pwd, pwdConf):
        if pwd != pwdConf:
            msg = forms.ValidationError(self.PASSWORD_CONF_NOT_EQUAL_MSG)
            self.add_error('password', msg)
            self.add_error('passwordConf', msg)


    def birthDateChecksNatNum(self, natNum, bdate):
        if bdate:
            natNum = natNum.replace("-", ".")
            natNumSplitted = natNum.split(".")
            natnumList = [natNumSplitted[0], natNumSplitted[1], natNumSplitted[2]]
            bdateList = [bdate.strftime("%Y")[2:4], bdate.strftime("%m"), bdate.strftime("%d")]

            if bdateList != natnumList:
                msg = forms.ValidationError(self.NAT_NUM_COMPARED_TO_B_DATE_MSG)
                self.add_error('birthDate', msg)
                self.add_error('nationalNumber', msg)


    def postalCodeChecksTown(self, town, postalCode):
        path = '{}/{}'.format(settings.STATICFILES_DIRS[0], 'localitiesAndPostalCodes.txt')
        with open(path) as myFile:
            dataRaw = myFile.read()
            locAndPostCodesDict = ast.literal_eval(dataRaw)

            if locAndPostCodesDict:
                locList = [key for key,val in locAndPostCodesDict.items() if val == postalCode]

            if not town in locList:
                msg = forms.ValidationError(self.LOCALITY_COMPARED_TO_P_CODE_MSG)
                self.add_error('postalCode', msg)
                self.add_error('town', msg)


    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        passwordConf = cleaned_data.get('passwordConf')
        natNum = cleaned_data.get('nationalNumber')
        bdate = cleaned_data.get('birthDate')
        postalCode = cleaned_data.get('postalCode')
        town = cleaned_data.get('town')

        self.birthDateChecksNatNum(natNum, bdate)
        self.passwordEqualsPasswordConf(password, passwordConf)
        self.postalCodeChecksTown(town, postalCode)

        return cleaned_data



class MyUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = (
            'is_admin',
            'is_active',
            'is_staff',
            'is_superuser',
            'nationalNumber',
            'lastName',
            'firstName',
            'birthDate',
            'password',
            'email',
            'username',
            'isOwner',
            'isHost',
            'isSponsor',
        )

        labels = {
            'phoneNumber':  _('Téléphone'),
            'streetNumber': _('Numéro'),
            'streetName':   _('Rue'),
            'town':         _('Ville'),
            'postalCode':   _('Code postale'),
        }

        error_messages = {
            # 'lastName': {
            #     'max_length': _("Nom trop long."),
            # },
            # 'firstName': {
            #     'max_length': _("Prénom trop long."),
            # },
        }

        help_texts = {}