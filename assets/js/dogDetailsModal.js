function showDogDetails(dogId) {
    $.get(`/dogs/dogDetails/${dogId}`, res => {
        const parsedDog = $.parseJSON(res);
        const dog = parsedDog[0].fields;

        $('#detailsModal .modal-title').html(`${dog.name}`);

        $('#detailsModal .modal-body').html(
            `<img class="img-fluid" src="//npe/assets/img/${dog.picture}"
                style="max-width: 100%;
                height: auto;" alt="photo de ${dog.name}">`
        );
        $('#detailsModal .modalCancelBtn').html('fermer');
    });
}