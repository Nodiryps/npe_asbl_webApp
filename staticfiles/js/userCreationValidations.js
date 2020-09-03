$(() => {

    validatorsUserCreation();
    validationUserCreation();

});


let NATIONAL_NMBR_STR = '';
let BIRTH_DATE_STR = '';

const MIN_AGE_TO_SUB = 18

const MIN_LENGTH_USERNAME = 5;
const MAX_LENGTH_USERNAME = 30;

const MIN_LENGTH_PHONE_NUMBER = 12;
const MAX_LENGTH_PHONE_NUMBER = 13;

const MIN_LENGTH_STREET_NUMBER = 1;
const MAX_LENGTH_STREET_NUMBER = 4;

const POSTAL_CODE = 4;

const MIN_LENGTH_PASSWORD = 5;
const MAX_LENGTH_PASSWORD = 100;

const MIN_LENGTH_NATIONAL_NUMBER = 11;
const MAX_LENGTH_NATIONAL_NUMBER = 15;

const MIN_LENGTH_STREET_NAME = 9; //rue de qq

const MIN_LENGTH_DEFAULT = 2;
const MAX_LENGTH_DEFAULT = 60;

const REQUIRED_MSG = "Champ requis"
const NO_WHITE_SPACE_MSG = "Ne peut pas contenir d' \"espace(s)\"";
const PHONE_NMBER_FORMAT_MSG = "Format du numéro invalide";
const MAY_ONLY_CONTAINS = "Ne peut contenir que "
const DIGITS_ONLY_MSG = MAY_ONLY_CONTAINS + "des chiffres";
const PHONE_NUMBER_MSG = DIGITS_ONLY_MSG + " et doit commencer par un \"zéro\" (0)";
const CHARS_AND_PUNCT_MSG = MAY_ONLY_CONTAINS + "des lettres et et certains caractères spéciaux (\".\", \"-\", \"_\")";
const CHARS_PUNCT_AND_NULBERS_MSG = MAY_ONLY_CONTAINS + "des chiffres, des lettres et certains caractères spéciaux (\".\", \"-\", \"_\")";
const DIGITS_AND_PUNCT = MAY_ONLY_CONTAINS + " des chiffres et certains caractères spéciaux (\".\", \"-\")";
const NATIONAL_NUMBER_MSG = "Format invalide (ex.: 90.12.01-123.45)"
const UNICITY_MSG = "Déjà pris, pas assez rapide ;)";
const NAT_NUM_COMPARED_TO_B_DATE_MSG = "Incohérence entre la date de naissance et le numéro national"
const PASSWORD_CONF_NOT_EQUAL = "Les mots de passe doivent être identiques"
const PASSWORD_SPECS_MSG = MAY_ONLY_CONTAINS + "des lettres, des chiffres, et certains caractères spéciaux (ex.: \"+.,#&\")"
const BIRTH_DATE_VALIDITY_MSG = "Il faut, au moins, avoir 18 ans"


function errorMsgMaxLength(maxlength) {
    return `Trop long, allez-y doucement :) (max. ${maxlength})`;
}


function errorMsgMinLength(minlength) {
    return `Trop court, encore un petit effort :) (min. ${minlength})`;
}


function validatorsUserCreation() {
    $.validator.addMethod("noWhiteSpace", (value, elem) => {
        return /^[\S]*$/gm.test(value);
    });

    $.validator.addMethod("phoneNumberSpecs", (value, elem) => {
        return /^[0]+[0-9]+(?:[ ][0-9]+)*$/gm.test(value);
    });

    $.validator.addMethod("phoneNumberFormat", (value, elem) => {
        return isLandlineNumber(value) || isMobilePhoneNumber(value);
    });

    $.validator.addMethod("namesSpecs", (value, elem) => {
        // return /^[A-Za-z]+(?:[ '-][A-Za-z]+)*$/.test(value);
        return /^[^0-9_!¡?÷?¿/\\+=*@#$€@µ%&^°§²³`(){}|~<>;,:\[\]]*$/.test(value);
    });

    $.validator.addMethod("nationalNumberSpecs", (value, elem) => {
        return /^[0-9]+(?:[ ][0-9]+)*$/.test(value)
            || /^[0-9]{2}.[0-9]{2}.[0-9]{2}-[0-9]{3}.[0-9]{2}$/.test(value);
    });

    $.validator.addMethod("usernameSpecs", (value, elem) => {
        return /^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$/.test(value);
    });

    $.validator.addMethod("passwordSpecs", (value, elem) => {
    return /^[A-Za-z0-9]+(?:[ '=*/+-.,;:/$µ£_!?~%&#§°]+)*$/.test(value);
    });

    $.validator.addMethod("birthDateCompareToNatNum", (value, elem) => {
        return birthDateCompareToNatNum();
    });

    $.validator.addMethod("isBirthDateValid", (value, elem) => {
        return isBirthdateValidDatePicker()
            || isBirthDateValidTextInput();
    });
}

function birthDateCompareToNatNum() {
    return BIRTH_DATE_STR === NATIONAL_NMBR_STR;
}


function getNatNumStringFormat() {
    const id_nationalNumber = $('#id_nationalNumber');
    let num = removeWhiteSpaces(id_nationalNumber.val());
    const pattern = /^[0-9]{2}.[0-9]{2}.[0-9]{2}-[0-9]{3}.[0-9]{2}$/;

    if (pattern.test(num)) {
        NATIONAL_NMBR_STR = [num.slice(0, 2), num.slice(3, 5), num.slice(6, 8)].join('');
    }
}


function getBirthDateStringFormat() {
    let bdate = $('#id_birthDate').datepicker('getDate', true);
    // BIRTH_DATE_STR = [bdate.slice(2, 4), bdate.slice(5, 7), bdate.slice(8)].join('');
    BIRTH_DATE_STR = [bdate.slice(8), bdate.slice(3, 5), bdate.slice(0, 2)].join('');
}


function isBirthDateValidTextInput() {
    let bool = false;
    const res = isBirthDateValidMngmnt()

    if (res){
        bool = res >= MIN_AGE_TO_SUB;
    }

    return bool;
}


function isBirthdateValidDatePicker() {
    let cptDatePicker = 3;
    let bool = false;

    $('#id_birthDate').on('pick.datepicker', () => {
        cptDatePicker--;

        if(cptDatePicker === 0){
            bool = isBirthDateValidMngmnt() >= MIN_AGE_TO_SUB;
        }
    });

    return bool;
}


function isBirthDateValidMngmnt() {
    let res = '';
    const today = new Date($.now());
    const todayString = today.getFullYear()*10000 + today.getMonth()*100 + today.getDay();
    const bdate = $('#id_birthDate').datepicker('getDate', true);
    // const bdateStr = [bdate.slice(0, 4), bdate.slice(5, 7), bdate.slice(8)].join('');
    const bdateStr = [bdate.slice(6), bdate.slice(3, 5), bdate.slice(0, 2)].join('');
    const todayMinusBDate = todayString - bdateStr;

    if (bdate.slice(0, 4) >= today.getFullYear() - 10) {
        res = `${todayMinusBDate}`.slice(0,1);
    } else {
        res = `${todayMinusBDate}`.slice(0,2);
    }

    return res;
}


function validationUserCreation() {
    $('#userCreationForm').validate({
        rules: {
            lastname: {
                required: true,
                minlength: MIN_LENGTH_DEFAULT,
                maxlength: MAX_LENGTH_DEFAULT,
                namesSpecs: true
            },
            firstname: {
                required: true,
                minlength: MIN_LENGTH_DEFAULT,
                maxlength: MAX_LENGTH_DEFAULT,
                namesSpecs: true
            },
            birthDate: {
                required: true,
                isBirthDateValid: true,
                // birthDateCompareToNatNum: true,
            },
            email: {
                required: true,
                minlength: MIN_LENGTH_DEFAULT,
                maxlength: MAX_LENGTH_DEFAULT,
                remote: "/accounts/isEmailUnique/"
            },
            phoneNumber: {
                required: true,
                minlength: MIN_LENGTH_PHONE_NUMBER,
                maxlength: MAX_LENGTH_PHONE_NUMBER,
                phoneNumberSpecs: true,
                phoneNumberFormat: true,
                remote: "/accounts/isPhoneNumberUnique/"
            },
            streetName: {
                required: true,
                minlength: MIN_LENGTH_STREET_NAME,
                maxlength: MAX_LENGTH_DEFAULT,
                namesSpecs: true
            },
            streetNumber: {
                required: true,
                minlength: MIN_LENGTH_STREET_NUMBER,
                maxlength: MAX_LENGTH_STREET_NUMBER
            },
            postalCode: {
                required: true,
                // minlength: POSTAL_CODE,
                // maxlength: POSTAL_CODE,
                noWhiteSpace: true
            },
            town: {
                required: true,
                // minlength: MIN_LENGTH_DEFAULT,
                // maxlength: MAX_LENGTH_DEFAULT,
                namesSpecs: true
            },
            nationalNumber: {
                required: true,
                minlength: MIN_LENGTH_NATIONAL_NUMBER,
                maxlength: MAX_LENGTH_NATIONAL_NUMBER,
                nationalNumberSpecs: true,
                birthDateCompareToNatNum: true,
                remote: "/accounts/isNationalNumberUnique/"
            },
            // username: {
            //     required: true,
            //     minlength: MIN_LENGTH_USERNAME,
            //     maxlength: MAX_LENGTH_USERNAME,
            //     usernameSpecs: true,
            //     remote: "/accounts/isUsernameUnique/"
            // },
            password: {
                required: true,
                minlength: MIN_LENGTH_PASSWORD,
                maxlength: MAX_LENGTH_PASSWORD,
                passwordSpecs: true
            },
            passwordConf: {
                required: true,
                minlength: MIN_LENGTH_PASSWORD,
                maxlength: MAX_LENGTH_PASSWORD,
                equalTo: '#id_password',
                passwordSpecs: true
            },
        },
        messages: {
            lastname: {
                required: REQUIRED_MSG,
                minlength: errorMsgMinLength(MIN_LENGTH_DEFAULT),
                maxlength: errorMsgMaxLength(MAX_LENGTH_DEFAULT),
                namesSpecs: CHARS_AND_PUNCT_MSG
            },
            firstname: {
                required: REQUIRED_MSG,
                minlength: errorMsgMinLength(MIN_LENGTH_DEFAULT),
                maxlength: errorMsgMaxLength(MAX_LENGTH_DEFAULT),
                namesSpecs: CHARS_AND_PUNCT_MSG
            },
            birthDate: {
                required: REQUIRED_MSG,
                birthDateCompareToNatNum: NAT_NUM_COMPARED_TO_B_DATE_MSG,
                isBirthDateValid: BIRTH_DATE_VALIDITY_MSG
            },
            email: {
                required: REQUIRED_MSG,
                minlength: errorMsgMinLength(MIN_LENGTH_DEFAULT),
                maxlength: errorMsgMaxLength(MAX_LENGTH_DEFAULT),
                email: "Email invalide",
                remote: UNICITY_MSG
            },
            phoneNumber: {
                required: REQUIRED_MSG,
                minlength: errorMsgMinLength(MIN_LENGTH_PHONE_NUMBER),
                maxlength: errorMsgMaxLength(MAX_LENGTH_PHONE_NUMBER),
                phoneNumberSpecs: PHONE_NUMBER_MSG,
                phoneNumberFormat: PHONE_NMBER_FORMAT_MSG,
                remote: UNICITY_MSG
            },
            streetName: {
                required: REQUIRED_MSG,
                minlength: errorMsgMinLength(MIN_LENGTH_STREET_NAME),
                maxlength: errorMsgMaxLength(MAX_LENGTH_DEFAULT),
                namesSpecs: CHARS_AND_PUNCT_MSG
            },
            streetNumber: {
                required: REQUIRED_MSG,
                minlength: errorMsgMinLength(MIN_LENGTH_STREET_NUMBER),
                maxlength: errorMsgMaxLength(MAX_LENGTH_STREET_NUMBER)
            },
            postalCode: {
                required: REQUIRED_MSG,
                noWhiteSpace: NO_WHITE_SPACE_MSG
            },
            town: {
                required: REQUIRED_MSG,
                namesSpecs: CHARS_AND_PUNCT_MSG
            },
            nationalNumber: {
                required: REQUIRED_MSG,
                minlength: errorMsgMinLength(MIN_LENGTH_NATIONAL_NUMBER),
                maxlength: errorMsgMaxLength(MAX_LENGTH_NATIONAL_NUMBER),
                nationalNumberSpecs: NATIONAL_NUMBER_MSG,
                birthDateCompareToNatNum: NAT_NUM_COMPARED_TO_B_DATE_MSG,
                remote: UNICITY_MSG
            },
            // username: {
            //     required: REQUIRED_MSG,
            //     minlength: errorMsgMinLength(MIN_LENGTH_USERNAME),
            //     maxlength: errorMsgMaxLength(MAX_LENGTH_USERNAME),
            //     usernameSpecs: CHARS_PUNCT_AND_NULBERS_MSG,
            //     remote: UNICITY_MSG
            // },
            password: {
                required: REQUIRED_MSG,
                minlength: errorMsgMinLength(MIN_LENGTH_PASSWORD),
                maxlength: errorMsgMaxLength(MAX_LENGTH_PASSWORD),
                passwordSpecs: PASSWORD_SPECS_MSG
            },
            passwordConf: {
                required: REQUIRED_MSG,
                minlength: errorMsgMinLength(MIN_LENGTH_PASSWORD),
                maxlength: errorMsgMaxLength(MAX_LENGTH_PASSWORD),
                equalTo: PASSWORD_CONF_NOT_EQUAL,
                passwordSpecs: PASSWORD_SPECS_MSG
            },
        }
    });
}