$(() => {

    window.onload = $('#searchbar').val(''); // to clear input on page refresh

    const dog_list = $('#dogList');

    $('#searchbar').on('keyup', () => {
        $.get(`/dogs/?query=${$('#searchbar').val()}`)
            .done(res => {
                dog_list.fadeTo('fast', 0)
                .promise().then(() => {
                        dog_list.html(res['html_from_view']);
                        dog_list.fadeTo('fast', 1);
                    });
            });
    });

});


function gndrFltr(gender) {
    const dog_list = $('#dogList');

    $.get(`/dogs/?genderFilter=${gender}`, res => {
        dog_list.fadeTo('fast', 0)
            .promise().then(() => {
                dog_list.html(res['html_from_view']);
                dog_list.fadeTo('fast', 1);
            });
    });

    $('#searchbar').focus();
}