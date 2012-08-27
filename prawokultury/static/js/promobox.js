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


$switchers.each(function(i, e) {
    $(e).click(function(e) {
        e.preventDefault();
        change_slide(i);
    });
});


var timeout = null;
var cycle_slide = function() {
    var current = $slides.filter('.active').index();
    change_slide((current + 1) % $slides.length);
}
var reset_timeout = function() {
    clearTimeout(timeout);
    timeout = setTimeout(cycle_slide, 5000);
};
timeout = setTimeout(cycle_slide, 3000);


});