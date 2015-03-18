// site/js/admin/collections/projects.js

var app = app || {};

app.Projects = Backbone.Collection.extend({
	model: app.Project,
	url: '/projects.json'
});
