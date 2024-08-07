{
    'name': 'mfb',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Mada Fiara Be',
    'description': 'Mada Fiara Be',
    'author': 'Matthieu',
    'website': 'http://www.example.com',
    'depends': ['base', 'sale', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'cron/ir_cron.xml',
        'views/mfb_models_views.xml',
        'views/mfb_custom_layout.xml',
        'reports/mfb_reports.xml',
        'reports/mfb_sale_order_report.xml',
        'reports/mfb_account_move_report.xml'
    ],
    'assets': {
        'web.report_assets_common': [
            'mfb/static/src/css/custom.css',
            '/mfb/static/src/css/fonts.css',
        ],

    },
    'installable': True,
    'application': True,
}