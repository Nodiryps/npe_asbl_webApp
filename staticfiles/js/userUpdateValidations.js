$(() => {

    validationUserUpdate();

});


function validationUserUpdate() {
    $('#userUpdateForm').validate({
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
                birthDateCompareToNatNum: true
            },
            email: {
                required: true,
                minlength: MIN_LENGTH_DEFAULT,
                maxlength: MAX_LENGTH_DEFAULT,
            },
            phoneNumber: {
                required: true,
                minlength: MIN_LENGTH_PHONE_NUMBER,
                maxlength: MAX_LENGTH_PHONE_NUMBER,
                phoneNumberSpecs: true,
                phoneNumberFormat: true
            },
            streetName: {
                required: true,
                minlength: MIN_LENGTH_DEFAULT,
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
                noWhiteSpace: true
            },
            town: {
                required: true,
                namesSpecs: true
            },
            nationalNumber: {
                required: true,
                minlength: MIN_LENGTH_NATIONAL_NUMBER,
                maxlength: MAX_LENGTH_NATIONAL_NUMBER,
                nationalNumberSpecs: true,
                birthDateCompareToNatNum: true
            },
            username: {
                required: true,
                minlength: MIN_LENGTH_USERNAME,
                maxlength: MAX_LENGTH_USERNAME,
                usernameSpecs: true,
                remote: "/accounts/isUsernameUnique/"
            },
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
                birthDateCompareToNatNum: NAT_NUM_COMPARED_TO_B_DATE_MSG
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
                phoneNumberSpecs: DIGITS_ONLY_MSG,
                phoneNumberFormat: PHONE_NMBER_FORMAT_MSG
            },
            streetName: {
                required: REQUIRED_MSG,
                minlength: errorMsgMinLength(MIN_LENGTH_DEFAULT),
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
                birthDateCompareToNatNum: NAT_NUM_COMPARED_TO_B_DATE_MSG
            },
            username: {
                required: REQUIRED_MSG,
                minlength: errorMsgMinLength(MIN_LENGTH_USERNAME),
                maxlength: errorMsgMaxLength(MAX_LENGTH_USERNAME),
                usernameSpecs: CHARS_PUNCT_AND_NULBERS_MSG,
                remote: UNICITY_MSG
            },
            password: {
                required: REQUIRED_MSG,
                minlength: errorMsgMinLength(MIN_LENGTH_PASSWORD),
                maxlength: errorMsgMaxLength(MAX_LENGTH_PASSWORD),
                // passwordSpecs: PASSWORD_SPECS
            },
            passwordConf: {
                required: REQUIRED_MSG,
                minlength: errorMsgMinLength(MIN_LENGTH_PASSWORD),
                maxlength: errorMsgMaxLength(MAX_LENGTH_PASSWORD),
                equalTo: PASSWORD_CONF_NOT_EQUAL,
                // passwordSpecs: PASSWORD_SPECS
            },
        }
    });
}