function sendDemand(idDog, idUser, dogName, demandType) {
    let url = `/demands/newDemand/${idDog}/${idUser}/${demandType}/`;

    setHtmlModal(dogName, demandType, 'sendDemand');

    // empty the id when close/cancel modal or it'll keep
    // and send the previous canceled requests
    $('.modalCancelBtn, .close').on('click', () => {
        url = '';
    });

    if (url !== '') {
        $('.modalConfirmBtn').on('click', () => {
            disableSendDemandBtns();
            ajaxSetup();
            ajaxPostNewDemand(url, demandType)
                .promise().then(() => {
                    badgeNotification();
                });
        });
    }
}


function ajaxPostNewDemand(url, demandType) {
    return $.post(url, res => {
        if (res) {
            $('.toast').toast('show');

            setTimeout(() => {
                window.location = '/'
            }, 3000);

            hideBtns(demandType);
        }
    });
}


function hideBtns(demandType) {
    setTimeout(() => {
        if (demandType === 'adoption')
            $('.divAdoptionBtn').hide();
        else if (demandType === 'hosting')
            $('.divHostBtn').hide();
        else if (demandType === 'sponsor')
            $('.divSponsorBtn').hide();
    }, 3500);
}


function disableSendDemandBtns() {
    $('.divAdoptionBtn a').replaceWith(
        `<a class="btn btn-sm adoptionBtn" title="adopter un chien">
            <i class="fas fa-heart"></i> Adopter
        </a>`
    );

    $('.divHostBtn a').replaceWith(
        `<a class="btn btn-sm hostBtn" title="accueillir un chien">
                <i class="fas fa-home"></i> Accueillir
        </a>`
    );
}


function acceptDemandConfirmModal(idDemand, idDog, dogName, demandType) {
    let url = `/demands/acceptDemand/${idDemand}/`;

    setHtmlModal(dogName, demandType, 'acceptDemand');

    // empty the id when close/cancel modal or it'll keep
    // and send the previous canceled requests
    $('.modalCancelBtn, .close').on('click', () => {
        url = '';
    });

    if (url !== '') {
        $('.modalConfirmBtn').on('click', () => {
            ajaxSetup();
            ajaxGetHostDemandByDog(idDog)
                .then(() => {
                    ajaxPostAcceptDemand(url, idDemand)
                })
                .then(() => {
                    badgeNotification();
                });
        });
    }
}


function ajaxPostAcceptDemand(url, id) {
    return $.post(url, res => {
        if (res) {
            const row = $('#id_demand_' + id).parent('tr');
            row.hide(250);
            $('.toast').toast('show');
        }
    });
}


function ajaxGetHostDemandByDog(idDog) {
    return $.get(`/demands/getHostDemandByDog/${idDog}`, res => {
        if (res && res !== '') {
            const row = $('#id_demand_' + res).parent('tr');
            row.hide(250);
        }
    });
}


function setHtmlModal(dogName, demandType, operation) {
    if (demandType === 'hosting') {
        demandType = 'accueil';
    }

    if (operation === 'sendDemand') {
        setHtmlSendDemand(demandType, dogName);
    } else if (operation === 'acceptDemand') {
        setHtmlAcceptDemand(demandType, dogName);
    }
}


function setHtmlSponsorDog(dogName) {
    $('#confirmModal .modal-title').html(`Vous êtes sur le point de <u>parrainer</u> <b>${dogName}</b>`);
    $('#confirmModal .modal-body').html(
        `Sélectionnez le type de parrainage souhaité.
        <br><br><b>complet</b>: <u>25€</u> et <b>demi-parrainage</b>: <u>12,50€</u>.`
    );

    $('#confirmModal .modal-footer').html(
        `<button type="button" class="modalCancelBtn btn btn-outline-secondary" data-dismiss="modal">
            annuler
        </button>
        <button type="button" class="modalHalfBtn btn btn-secondary" data-amount="12.50" onclick="payment();">
            demi-parrainage
        </button>
        <button type="button" class="modalCompletBtn btn btn-secondary" data-amount="25" onclick="payment();">
            parrainage complet
        </button>`
    );
}


function setHtmlSendDemand(demandType, dogName) {
    $('#confirmModal .modal-title').html(`Envoi de demande d'` + demandType);
    $('#confirmModal .modal-body').html(`Êtes-vous sûr.e de vouloir envoyer une demande d'<u>` + demandType + `</u> pour <b>` + dogName + `</b> ?`);
    $('#confirmModal .modalCancelBtn').html('annuler');
    $('#confirmModal .modalConfirmBtn').html('envoyer');
    $('.toast-body').html(`Votre demande a bien été envoyée :)`);
}


function setHtmlAcceptDemand(demandType, dogName) {
    $('#confirmModal .modal-title').html(`Validation de demande d'` + demandType);
    $('#confirmModal .modal-body').html(`Êtes-vous sûr.e de vouloir accepter la demande d'<u>` + demandType + `</u> pour <b>` + dogName + `</b> ?`);
    $('#confirmModal .modalCancelBtn').html('annuler');
    $('#confirmModal .modalConfirmBtn').html('accepter');
    $('#confirmModal .modalConfirmBtn').css('backgroundColor', 'rgb(179, 154, 230)');
    $('#confirmModal .modalConfirmBtn').css('borderColor', 'rgb(179, 154, 230)');
    $('#confirmModal .modalConfirmBtn').hover((e) => {
        $('#confirmModal .modalConfirmBtn').css('backgroundColor',
            e.type === 'mouseenter' ? 'rgb(125, 85, 204)' : 'rgb(179, 154, 230)')
        $('#confirmModal .modalConfirmBtn').css('borderColor',
            e.type === 'mouseenter' ? 'rgb(125, 85, 204)' : 'rgb(179, 154, 230)');
    });
    $('.toast-body').html(`La demande a bien été acceptée :)`);
}