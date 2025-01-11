{
    'name': 'mfb_dashboard_analytics',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Mada Fiara Be Dashboard',
    'description': 'Mada Fiara Be Partner Discount',
    'author': 'Mihaja',
    'website': 'http://www.example.com',
    'depends': ['base', 'sale_management', 'hr_expense'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/mfb_sale_order.xml',
        'views/dashboard.xml'
    ],
    'installable': True,
    'application': True,
}