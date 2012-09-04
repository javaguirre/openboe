(function() {
    var TEMPLATE_URL = '/static';

    var Link = Backbone.Model.extend({
    });

    var LinkList = Backbone.Collection.extend({

        model: Link,
        url: function() {
            if(!this.query)
                return '/links/?feed=' + this.feed;
            else
                return '/links/?feed=' + this.feed + "&q=" + this.query;
        },

        initialize: function(options) {
            this.feed = options.feed;
            this.query = options.query;
        },

        fetch: function(options) {
            options || (options = {});

            if(options.hasOwnProperty('query')) {
                this.setQuery(options.query);
            }

            return Backbone.Collection.prototype.fetch.call(this, options);
        },

        setQuery: function(query) {
            this.query = query;
        },

        setFeed: function(feed) {
            this.feed = feed;
        }
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

        events: {
            "click #search-button": "performSearch"
        },

        initialize: function(options) {
            var self = this,
                parentElt = options.appendTo || $('.body-container');

            TEMPLATE_URL = options.templateUrl || TEMPLATE_URL;

            parentElt.template(TEMPLATE_URL + '/templates/app.html', {}, function() {
                self.el = $('#openboeapp');
                self.delegateEvents();

                self.links = new LinkList({feed: options.feed,
                                           query: options.query
                                          });
                self.links.bind('add',   self.addOne, self);
                self.links.bind('reset', self.addAll, self);
                self.links.bind('all',   self.render, self);

                self.section = options.section;
                self.feed = options.feed;

                self.links.fetch({feed: options.feed});
                /*self.setFeedHeader(this.feed);*/
                self.setSearchAction(options.section, options.feed);
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
            var feed_title = feed.replace(/\-/g, " ");
            feed_title = feed_title.charAt(0).toUpperCase() + feed_title.slice(1);
            this.$('.section-header').text(feed_title);
        },

        setSearchAction: function(section, feed) {
            this.$('#search-form').attr('action', "/#!/" + section + "/" + feed);
        },

        performSearch: function(e) {
            query = $('input[name="q"]').val();
            this.links.fetch({feed: this.feed, query: query});
            Backbone.history.navigate("!/" + this.section + "/" + this.feed + "/" + query, true);
        }
    });

    window.MyRouter = Backbone.Router.extend({
        routes: {
            "!/": "index",
            "!/:section/:feed": "feed_items",
            "!/:section/:feed/:query" : "feed_items"
        },

        index: function() {
            console.log("This is the index!");
        },

        feed_items: function(section, feed, query) {
            var myquery = query || "";
            var view = new LinkApp({feed: feed,
                                    section: section,
                                    query: myquery,
                                   });
        }
    });
}());
