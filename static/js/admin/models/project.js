// site/js/admin/models/project.js

var app = app || {};

app.Project = Backbone.Model.extend({
	defaults: {
		id: 'Umm..'
		title: 'Not here',
		url: 'Unknown',
		blurb: 'blurb',
		description: 'Unknown',
		keywords: 'None'
	}
});
