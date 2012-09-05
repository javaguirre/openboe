$(function () {
    $('.mainbar li a').click(function() {
        var href = "#tab-" + $(this).attr('href').replace("#", "");

        console.log(href);

        $('.mainbar li').removeClass('active');
        $('.tab-pane').removeClass('active');

        $(this).parent().addClass('active');
        $(href).addClass('active');
    });
});
