(function($) {
    $(function() {


var have_localstorage;
try {
    localStorage.setItem("test", "test");
    localStorage.removeItem("test");
    have_localstorage = true;
} catch(e) {
    have_localstorage = false;
}



$("#annoy-on").click(function(e) {
    e.preventDefault();
    $("#annoy").slideDown('fast');
    $(this).hide();
    if (have_localstorage) localStorage.removeItem("annoyed2013");
});

$("#annoy-off").click(function() {
    $("#annoy").slideUp('fast');
    $("#annoy-on").show();
    if (have_localstorage) localStorage["annoyed2013"] = true;
});


if (have_localstorage) {
    if (!localStorage["annoyed2013"]) {
        $("#annoy-on").hide();
        $("#annoy").show();
    }
}



    });
})(jQuery);
