$(function () {
    $('.nav-tabs li a').click(function() {
        var href = $(this).attr('href');
        $('.tab-pane').removeClass('active');
        $(href).addClass('active');
    });
});
