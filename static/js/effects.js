$(function () {
    $('.nav-tabs li a').click(function() {
        var href = $(this).attr('href');

        $('.nav-tabs li').removeClass('active');
        $('.tab-pane').removeClass('active');

        $(this).parent().addClass('active');
        $(href).addClass('active');
    });
});
