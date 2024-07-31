{
    'name': 'mfb_pricing_in_documents',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Mada Fiara Be Pricing in documents',
    'description': 'Mada Fiara Be Pricing in documents',
    'author': 'Matthieu',
    'website': 'http://www.example.com',
    'depends': ['base', 'sale'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/mfb_sale_order.xml',
        'cron/set_included_tax.xml'
    ],
    'installable': True,
    'application': True,
}