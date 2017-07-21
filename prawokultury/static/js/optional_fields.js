/* globals travelGrantCountries */

$(document).ready(function() {

    var countrySelect = $('#id_country');
    var grantCheckbox = $('#id_travel_grant');
    countrySelect.on('change', function () {
        var goodCountry = $.inArray($(this).val(), travelGrantCountries) > -1;
        grantCheckbox.closest('tr').toggle(goodCountry);
        if (!goodCountry) {
            grantCheckbox.prop('checked', false);
            grantCheckbox.trigger('change');
        }
    });
    grantCheckbox.on('change', function () {
        var checked = Boolean(this.checked);
        $('#id_travel_grant_motivation').closest('tr').toggle(checked);
    });
    countrySelect.trigger('change');
    grantCheckbox.trigger('change');

});
