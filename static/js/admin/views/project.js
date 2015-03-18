// site/js/admin/views/project.js

var app = app || {};

app.ProjectView = Backbone.View.extend({
		tagName: 'div',
		className: 'project',
		template: _.template( $('#projectTemplate').html() ),
		events: {
			'click .delete': 'deleteFilm'
		},

		deleteFilm: function () {
			// delete model...
			this.model.destroy();
			// delete view...
			this.remove();
		},

		render: function() {

			this.$el.html( this.template( this.model.toJSON() ));

			return this;
		}
	
});
