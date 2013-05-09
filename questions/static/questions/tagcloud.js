$(function() {
    var showTagsGroup = function(category_id) {
        $('.questions-tags-group').hide();
        $('.questions-tags-group[data-category-id=' + category_id +']').show();
    }
    $('#questions-categories a').click(function(e) {
        e.preventDefault();
        var target = $(e.target);
        if(target.hasClass('selected'))
            return;
        var category_id = target.attr('data-category-id');
        $('#questions-categories a').removeClass('selected');
        target.addClass('selected');
        showTagsGroup(category_id);
    });
    var selected = $('#questions-categories a.selected');
    if(selected) {
        var category_id = selected.attr('data-category-id');
        showTagsGroup(category_id);
    }
});