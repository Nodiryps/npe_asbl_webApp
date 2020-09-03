function userDetailsModal(id) {
    $.get(`/accounts/userDetails/${id}/`, res => {
        const parsedUser = $.parseJSON(res);
        const user = parsedUser[0].fields;

        $('#detailsModal .modal-title').html('<b>Infos du membre:</b><br> ' + user.username + '');

        $('#detailsModal .modal-body').css('margin', '0 auto 0 auto');
        $('#detailsModal .modal-body').css('text-align', 'center');
        $('#detailsModal .modal-title').css('text-align', 'center');
        $('#detailsModal .modal-title').css('margin', '0 auto ');

        $('#detailsModal .modal-body').html(
            `<b>Nom:</b><br> ${user.lastName} <br><br>
             <b>Prénom:</b><br> ${user.firstName} <br><br>
             <b>Né.e le:</b><br> ${getBirthDate(user.birthDate)} <br><br>
             <b>Numéro national:</b><br> ${user.nationalNumber} <br><br>
             <b>Email:</b><br> ${user.email} <br><br>
             <b>Tél.:</b><br> ${user.phoneNumber} <br><br>
             <b>Adresse:</b><br> ${user.streetNumber} ${user.streetName}, ${user.postalCode} ${user.town}`
        );

        $('#detailsModal .modalCancelBtn').html('fermer');
    });
}


function getBirthDate(bdate) {
    return [bdate.slice(8), bdate.slice(5, 7), bdate.slice(0, 4)].join('/');
}