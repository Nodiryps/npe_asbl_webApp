function userDeleteConfirmModal(id, name) {
    setHtmlDelete(name, 'user');
    let url = `/accounts/userDelete/${id}/`;

    // empty the id when close/cancel modal or it'll keep
    // and send the previous canceled requests
    $('.modalCancelBtn, .close').on('click', () => {
        url = '';
    });

    if (url !== '') {
        $('.modalConfirmBtn').on('click', () => {
            ajaxSetup();
            return $.post(url, result => {
                if (result) {
                    const row = $('#id_user_' + id).parent('tr');
                    row.hide(250);
                    $('.toast').toast('show');
                }
            });
        });
    }
}


function dogDeleteConfirmModal(id, name) {
    setHtmlDelete(name, 'dog');
    let url = `/dogs/dogDelete/${id}/`;

    // empty the id when close/cancel modal or it'll keep
    // and send the previous canceled requests
    $('.modalCancelBtn, .close').on('click', () => {
        url = '';
    });

    if (url !== '') {
        $('.modalConfirmBtn').on('click', () => {
            ajaxSetup();
            return $.post(url, result => {
                if (result) {
                    deleteDog(id);
                }
            });
        });
    }
}


function deleteDog(id) {
    $('#id_dog_' + id).hide()
        .promise().then(() => {
            $('.toast').toast('show');
            setTimeout(() => {
                window.location = '/'
            }, 3000);
        });
}


function demandDeleteConfirmModal(id, name) {
    setHtmlDelete(name, 'demand');
    let url = `/demands/deleteDemand/${id}/`;

    // empty the id when close/cancel modal or it'll keep
    // and send the previous canceled requests
    $('.modalCancelBtn, .close').on('click', () => {
        url = '';
    });

    if (url !== '') {
        $('.modalConfirmBtn').on('click', () => {
            ajaxSetup();
            deleteDemand(url, id);
        });
    }
}


function deleteDemand(url, id) {
    return $.post(url, result => {
        if (result) {
            const row = $('#id_demand_' + id).parent('tr');
            row.hide(250);
            $('.toast').toast('show');
            sessionStorage.setItem('demandNb', sessionStorage.getItem('demandNb')-1);
            badgeNotification();
        }
    });
}


function ajaxSetup() {
    return $.ajaxSetup({
        // called before ajax req
        beforeSend: function (xhr, settings) {
            // add to header if it's the curr website
            // relative URL & type POST
            if (!/^https?:.*/.test(settings.url) && settings.type == "POST") {
                // add header
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
}


function getCookie(token) {
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, token.length + 1) == (token + '=')) {
                return decodeURIComponent(cookie.substring(token.length + 1));
            }
        }
    }
}


function setHtmlDelete(name, model) {
    const modalTitle = $('#confirmModal .modal-title');
    const modalBody = $('#confirmModal .modal-body');
    const modalCancelBtn = $('#confirmModal .modalCancelBtn');
    const modalConfirmBtn = $('#confirmModal .modalConfirmBtn');
    const toastBody = $('.toast-body');

    if (model === 'dog' || model === 'user') {
        setHtmlUsersDogs(name, modalTitle, modalBody, modalCancelBtn, modalConfirmBtn, toastBody);
    }
    if(model === 'demand') {
        setHtmlDemands(modalTitle, modalBody, modalCancelBtn, modalConfirmBtn, toastBody);
    }
}


function setHtmlUsersDogs(name, modalTitle, modalBody, modalCancelBtn, modalConfirmBtn, toastBody) {
    modalTitle.html('Confirmez la suppression définitive');
    modalBody.html('Êtes-vous sûr de vouloir supprimer <b>' + name + '</b> ?');
    modalCancelBtn.html('annuler');
    modalConfirmBtn.html('supprimer');
    toastBody.html("<b>" + name + "</b>" + ' a bien été supprimé.e de la DB');
}


function setHtmlDemands(modalTitle, modalBody, modalCancelBtn, modalConfirmBtn, toastBody) {
    modalTitle.html('Confirmez le rejet de la demande');
    modalBody.html('Êtes-vous sûr de vouloir rejeter cette demande ?');
    modalCancelBtn.html('annuler');
    modalConfirmBtn.html('rejeter');
    toastBody.html("La demande a bien été rejetée");
}


// function deleteConfirmModal(id, name, model) {
//     setHtmlDelete(name, model);
//     let url = '';

//     if (model === 'dog') {
//         url = `/dogs/dogDelete/${id}/`;
//     }
//     else if (model === 'user') {
//         url = `/accounts/userDelete/${id}/`
//     }
//     else if (model === 'demand') {
//         url = `/demands/deleteDemand/${id}/`
//     }

//     // empty the id when close/cancel modal or it'll keep
//     // and send the previous canceled requests
//     $('.modalCancelBtn, .close').on('click', () => {
//         url = '';
//     });

//     if (url !== '') {
//         $('.modalConfirmBtn').on('click', () => {
//             ajaxPostDelete(id, url, model, name);
//         });
//     }
// }


// function ajaxPostDelete(id, url, model) {
//     ajaxSetup();
//     return $.post(url, result => {
//         if (result) {
//             let row = "";

//             if (model === 'dog') {
//                 deleteDog(id);
//             }
//             else if (model === 'user') {
//                 $('.toast').toast('show');
//                 row = $('#id_user_' + id).parent('tr');
//                 row.hide(250);
//             }
//             else if (model === 'demand') {
//                 $('.toast').toast('show');
//                 row = $('#id_demand_' + id).parent('tr');
//                 row.hide(250);
//             }
//         }
//     });
// }