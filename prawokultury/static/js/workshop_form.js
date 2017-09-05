$(document).ready(function() {

    var project_row = $('#id_w_nobre_question').closest('tr');

    var switcher = $('#id_w_nobre');

    if (!switcher.is(':checked'))
        project_row.hide();

    switcher.on('change', function(data) {
        console.log(data);
        project_row.toggle();
    })

});
