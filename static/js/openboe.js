(function() {
    var TEMPLATE_URL = '/static';

    var Link = Backbone.Model.extend({
    });

    var LinkList = Backbone.Collection.extend({

        model: Link,

        url: function() {
            var my_url = '/links/?feed=' + this.feed;

            if(this.query) {
                my_url += "&q=" + this.query;
            }

            if(this.params.hasOwnProperty('from')) {
                my_url += "&from=" + this.params.from + "&to=" + this.params.to;
            }

            return my_url;
        },

        initialize: function(options) {
            this.setOptions(options);
        },

        /*fetch: function(options) {
            options || (options = {});
            this.setOptions(options);

            return Backbone.Collection.prototype.fetch.call(this, options);
        },*/

        setQuery: function(query) {
            this.query = query;
        },

        setFeed: function(feed) {
            this.feed = feed;
        },

        setParams: function(params) {
            this.params = params;
        },

        setOptions: function(options) {
            if(options.hasOwnProperty('feed')) {
                this.setFeed(options.feed);
            }
            if(options.hasOwnProperty('query')) {
                this.setQuery(options.query);
            }
            if(options.hasOwnProperty('params')) {
                this.setParams(options.params);
            }
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
                                           query: options.query,
                                           params: options.params
                                          });
                self.links.bind('add',   self.addOne, self);
                self.links.bind('reset', self.addAll, self);
                self.links.bind('all',   self.render, self);

                self.section = options.section;
                self.feed = options.feed;

                self.links.fetch();
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
            from_date = $('input[name="from"]').val().replace(/\//g, "-");
            to_date = $('input[name="to"]').val().replace(/\//g, "-");

            var url = "!/" + this.section + "/" + this.feed + "/" + query;
            var links_options = {
                                    feed: this.feed,
                                    query: query,
                                };

            //FIXME provisional
            if(from_date && to_date) {
                url += "?from=" + from_date + "&to=" + to_date;
                links_options.params = {'from': from_date, 'to': to_date};
            }

            Backbone.history.navigate(url, {trigger: true});
        }
    });

    window.MyRouter = Backbone.Router.extend({
        routes: {
            "!/": "index",
            "!/:section/:feed": "feed_items",
            "!/:section/:feed/:query": "feed_items",
            "!/:section/:feed/:query?:params" : "feed_items"
        },

        index: function() {
            console.log("This is the index!");
        },

        feed_items: function(section, feed, query, params) {
            var myquery = query || "";
            var view = new LinkApp({
                                    feed: feed,
                                    section: section,
                                    query: myquery,
                                    params: this.extractParams(params)
                                   });
        },

        extractParams: function(params) {
            var params_object = {};

            if(!params){
                return params_object;
            }

            $.each(params.split('&'), function(index, value){
                if(value){
                    var param = value.split('=');
                    params_object[param[0]] = param[1];
                }
            });

            return params_object;
        }
    });
}());
