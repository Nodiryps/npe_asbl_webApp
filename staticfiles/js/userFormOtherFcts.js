$(() => {

    phoneNumberFormating();
    nationalNumberFormating();

    getTownFromPostalCode();
    getPostalCodeFromTown();

    $('#id_nationalNumber, #id_birthDate').on('focusout', () => {
        getNatNumStringFormat();
        getBirthDateStringFormat();
    });


    $('#createUserBtn').on('click', () => {
        generateUsername();
    });

    if (USERNAME !== '') {
        $('#id_username').val(USERNAME);
    }

});

let USERNAME = ''


function replaceSpecialCharsUsername(string) {
    string = string.replace(" ", '')
    string = string.replace("\'", '')
    string = string.replace("´", '')
    string = string.replace("-", '')
    return string.toLowerCase()
}


function generateUsername() {
    let lastname = replaceSpecialCharsUsername($('#id_lastName').val());
    let firstname = replaceSpecialCharsUsername($('#id_firstName').val());
    let birthdate = $('#id_birthDate').datepicker('getDate', true);

    if (lastname !== '' && firstname !== '' && birthdate !== '') {
        const bdate = birthdate.slice(0, 2) + birthdate.slice(3, 5);
        const name = firstname.slice(0, 2) + lastname;
        const username = [bdate, name].join('');

        $('#id_username').val(username);
    }
}


function nationalNumberFormating() {
    const id_nationalNumber = $('#id_nationalNumber');

    id_nationalNumber.on('focusout', () => {
        let num = removeWhiteSpaces(id_nationalNumber.val());
        let res = '';
        const regex = /^[0-9]*$/gm;

        if (regex.test(num) && num.length === 11) {
            let start = [num.slice(0, 2), num.slice(2, 4), num.slice(4, 6)].join('.');
            let end = [num.slice(6, 9), num.slice(9)].join('.');
            res = [start, end].join('-');
        }

        if (res !== '') {
            id_nationalNumber.val(res);
        }
    });
}


function phoneNumberFormating() {
    const id_phoneNumber = $('#id_phoneNumber');

    id_phoneNumber.on('focusout', () => {
        let num = removeWhiteSpaces(id_phoneNumber.val());
        let res = '';
        const regex = /^[0-9]+(?:[ ][0-9]+)*$/gm;

        if (regex.test(num)) {
            if (isMobilePhoneNumber(num)) {
                res = [num.slice(0, 4), num.slice(4, 6), num.slice(6, 8), num.slice(8)].join(' ');
            }
            else if (isLandlineNumber(num)) {
                res = landlineNumberMngmnt(num);
            }
        }

        if (res !== '') {
            id_phoneNumber.val(res);
        }
    });
}


function landlineNumberMngmnt(num) {
    let res = '';

    if (isBigCity(num)) {
        res = [num.slice(0, 2), num.slice(2, 5), num.slice(5, 7), num.slice(7, 9), num.slice(9)].join(' ');
    } else {
        res = [num.slice(0, 3), num.slice(3, 5), num.slice(5, 7), num.slice(7, 9), num.slice(9)].join(' ');
    }

    return res.trimEnd();
}


function getPostalCodeFromTown() {
    $('#id_town').on('change', () => {
        const town = $('#id_town').val()

        if (town !== '') {
            let postalCode = '';
            $.each(POSTAL_CODES, (key, val) => {

                if (key.toUpperCase() === town.toUpperCase()) {
                    postalCode = val;
                }
            });

            $('#id_postalCode').val(postalCode);
        }
    });
}


function getTownFromPostalCode() {
    $('#id_postalCode').on('change', () => {
        const postalCode = $('#id_postalCode').val()

        if (postalCode !== '') {
            let town = '';

            $.each(POSTAL_CODES, (key, val) => {

                if (val === postalCode) {
                    town = key;
                }
            });

            $('#id_town').val(town);
        }
    });
}


function removeWhiteSpaces(str) {
    return str.replace(/ /g, ''); // [\s\xA0]+ IE doesn't consider non-breaking spaces as white-spaces
}


function isBigCity(phoneNumber) {
    const array = ['02', '03', '04', '09'];
    const twoFirst = phoneNumber.slice(0, 2);

    return array.includes(twoFirst);
}


function isMobilePhoneNumber(num) {
    num = removeWhiteSpaces(num);
    return num.length === 10 && num.slice(0, 2) === '04';
}


function isLandlineNumber(num) {
    return removeWhiteSpaces(num).length === 9;
}