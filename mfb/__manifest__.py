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
        'views/mfb_custom_layout.xml'



    ],
    'installable': True,
    'application': True,
}