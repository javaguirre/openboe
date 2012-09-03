(function() {
    var TEMPLATE_URL = '/static';

    var Link = Backbone.Model.extend({
    });

    var LinkList = Backbone.Collection.extend({

        model: Link,
        url: function() {
            return '/links/?feed=' + this.feed;
        },

        initialize: function(options) {
            this.feed = options.feed;
        },
    });

    var LinkView = Backbone.View.extend({
        tagName:  "li",

        initialize: function(options) {
        },

        render: function() {
            var self = this;

            $(self.el).template(TEMPLATE_URL + '/templates/item.html', self.model.toJSON(), function() {
                self.setText();
            });

            return this;
        },

        setText: function() {
            var text = this.model.get('description');
            this.$('.todo-text').text(text);
        },
    });

    window.LinkApp = Backbone.View.extend({

        initialize: function(options) {
            var self = this,
                parentElt = options.appendTo || $('.footer');

            TEMPLATE_URL = options.templateUrl || TEMPLATE_URL;

            parentElt.template(TEMPLATE_URL + '/templates/app.html', {}, function() {
                self.el = $('#todoapp');
                self.delegateEvents();

                self.links = new LinkList({feed: options.feed});
                self.links.bind('add',   self.addOne, self);
                self.links.bind('reset', self.addAll, self);
                self.links.bind('all',   self.render, self);

                self.links.fetch({feed: options.feed});
            });
        },

        render: function() {
            var self = this;

            return this;
        },

        addOne: function(link) {
            var view = new LinkView({model: link});
            this.$("#todo-list").append(view.render().el);
        },

        addAll: function() {
            this.links.each(this.addOne);
        },
    });

    window.MyRouter = Backbone.Router.extend({
        routes: {
            "!/": "index",
            "!/:section/:feed": "feed_items"
        },

        index: function() {
            console.log("This is the index!");
        },

        feed_items: function(section, feed) {
            var view = new LinkApp({feed: feed});
        }
    });
}());
