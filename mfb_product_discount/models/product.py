from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'product.template'

    product_discount = fields.Float(string='Remise')