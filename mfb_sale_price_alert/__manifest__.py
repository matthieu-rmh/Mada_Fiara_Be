{
    'name': 'mfb_sale_price_alert',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Mada Fiara Be Sale Price Alert',
    'description': 'Mada Fiara Be Sale Price Alert',
    'author': 'Mihaja',
    'website': 'http://www.example.com',
    'depends': ['base', 'sale'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/mfb_sale_order.xml',
        'cron/sale_price_alert.xml'
    ],
    'installable': True,
    'application': True,
}