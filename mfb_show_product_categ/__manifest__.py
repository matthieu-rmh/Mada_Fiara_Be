{
    'name': 'mfb_show_product_categ',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Mada Fiara Be Show product category',
    'description': 'Mada Fiara Be Show product category',
    'author': 'Mihaja',
    'website': 'http://www.example.com',
    'depends': ['base', 'purchase', 'stock'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase.xml',
         'views/stock.xml',
    ],
    'installable': True,
    'application': True,
}