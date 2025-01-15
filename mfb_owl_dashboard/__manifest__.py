{
	"name" : "MFB Owl Dashboard",
	"version" : "1.0",
	"summary" : "MFB Owl Dashboard",
	"sequence" : 4,
	"license" : "LGPL-3",
	"author" : "Mihaja",
	"description" : """
		
	""",
	"depends" : ['base', 'web', 'sale', 'board'],
	"data" : [
		# "security/ir.model.access.csv",
		"views/dashboard.xml",
		# "views/dashboard_parameter.xml",
		# "data/dashboard_parameter_data.xml"
	],
	"assets": {
		'web.assets_backend': [
			'owl/static/src/components/**/*.js',
			'owl/static/src/components/**/*.xml',
			# 'owl/static/src/components/**/*.scss',
		]
	},
	"application" : True,
	"installable" : True,
	"auto_install" : False,
}