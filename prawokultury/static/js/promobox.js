$(document).ready(function(){

var $slides = $("ul.promobox li");
var $switchers = $("ul#promobox-switcher li");

var change_slide = function(slide_no) {
    var $slide = $($slides.get(slide_no));
    var $switcher = $($switchers.get(slide_no));

    $slides.filter('.active').fadeOut();
    $slides.filter('.active').removeClass('active');
    $switchers.filter('.active').removeClass('active');
    $slide.fadeIn();
    $slide.addClass('active');
    $switcher.addClass('active');
    reset_timeout();
};


var timeout = null;
var cycle_slide = function() {
    var current = $slides.filter('.active').index();
    change_slide((current + 1) % $slides.length);
}


var reset_timeout = function() {
    clearTimeout(timeout);
    timeout = setTimeout(cycle_slide, 5000);
};


if ($slides.length > 1) {
    $switchers.each(function(i, e) {
        $(e).click(function(e) {
            e.preventDefault();
            change_slide(i);
        });
    });

    timeout = setTimeout(cycle_slide, 3000);
}


/*
if (!$('#id_presentation').checked) {
        $('[id^="id_presentation_"]').parent().parent().hide();
}
if (!$('#id_workshop').checked) {
        $('[id^="id_workshop_"]').parent().parent().hide();
}

$('#id_presentation').change(function() {
    if (this.checked) {
        $('[id^="id_presentation_"]').parent().parent().show('slow');
    } else {
        $('[id^="id_presentation_"]').parent().parent().hide('slow');
    }
});

$('#id_workshop').change(function() {
    if (this.checked) {
        $('[id^="id_workshop_"]').parent().parent().show('slow');
    } else {
        $('[id^="id_workshop_"]').parent().parent().hide('slow');
    }
});
*/



});
