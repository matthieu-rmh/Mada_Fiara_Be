from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_discount = fields.Float(string='Remise')