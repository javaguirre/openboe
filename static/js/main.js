require(['ext/jquery', 'ext/jqueryui', 'bootstrap-dropdown', 'effects', 'ext/underscore', 'ext/backbone', 'template', 'openboe'], function() {
    $(document).ready(function() {
        window.router = new MyRouter();
        Backbone.history.start();
        /*window.App = new LinkApp({ appendTo: $('.footer') });*/
    });
});
