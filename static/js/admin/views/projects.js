// site/js/admin/views/library.js

var app = app || {};

app.ProjectsView = Backbone.View.extend({

		el: '#adminEdit',

		events: {
			'click #add':'addProject',
			'click #edit': 'editProject',
		},

		initialize: function() {
			this.collection = new app.Projects();
			this.collection.fetch({reset: true});
			this.render();
			this.$plist = $('#projects-list');
			this.$sklist = $('#skills-list');
			this.$clist = $('#contact-list');
			this.$blist = $('#bio-list');
			this.listenTo( this.collection, 'add', this.renderProject);
			this.listenTo( this.collection, 'reset', this.render );
		},

		render: function () {
			this.collection.each(function(project) {
				this.renderProject(project);
			}, this );
			// body...
		},

		renderProject: function(project) {
			var view = new app.ProjectView({ model: project });
			this.$plist.append(view.render().el);
		},

		addProject: function(e) {
			e.preventDefault();
			var formData = {};

			$('#addProject div').children('input').each( function(i, el) {
				if( $(el).val() != '') {
					formData[el.id] = $( el ).val();
				}
			});

			this.collection.add( new app.Project( formData ))
		}
	
});
