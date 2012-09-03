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
        tagName:  "div",

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
            var title = this.model.get('title');
            var link_link = this.model.get('link');
            var guid = this.model.get('guid');

            this.$('.item-description').text(text);
            this.$('.item-link').text(title);
            this.$('.item-link').attr('href', link_link);
            this.$('.pdf-item-link').attr('href', guid);
        },

    });

    window.LinkApp = Backbone.View.extend({

        initialize: function(options) {
            var self = this,
                parentElt = options.appendTo || $('.body-container');

            TEMPLATE_URL = options.templateUrl || TEMPLATE_URL;

            parentElt.template(TEMPLATE_URL + '/templates/app.html', {}, function() {
                self.el = $('#openboeapp');
                self.delegateEvents();

                self.links = new LinkList({feed: options.feed});
                self.links.bind('add',   self.addOne, self);
                self.links.bind('reset', self.addAll, self);
                self.links.bind('all',   self.render, self);

                self.links.fetch({feed: options.feed});
                /*self.setFeedHeader(this.feed);*/
            });
        },

        render: function() {
            var self = this;

            return this;
        },

        addOne: function(link) {
            var view = new LinkView({model: link});
            this.$("#link-list").append(view.render().el);
        },

        addAll: function() {
            this.links.each(this.addOne);
        },

        setFeedHeader: function(feed) {
            console.log(feed);
            var feed_title = feed.replace(/\-/g, " ");
            feed_title = feed_title.charAt(0).toUpperCase() + feed_title.slice(1);
            this.$('.section-header').text(feed_title);
        }
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
            var view = new LinkApp({feed: feed,
                                    section: section});
        }
    });
}());
