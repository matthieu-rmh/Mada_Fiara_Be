from odoo import models, fields
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class PaymentMethod(models.Model):
    _inherit = 'payment.method'

    image = fields.Image(
        required=False,
    )

class AccountTax(models.Model):
    _inherit = 'account.tax'

    def _action_deactivate_all_unrelevant_taxes(self):
        """
        Deactivate taxes having the next conditions : 
        type_tax_use = 'sale' and tax_scope = 'consu' and not (tax_group_id = 2 and price_include is true)
        """

        domain = [
            ('type_tax_use', '=', 'sale'),
            ('tax_scope', '=', 'consu'),
            '!', '&', ('tax_group_id', '=', 2),
                    ('price_include', '=', True)
                ]

        taxes = self.env['account.tax'].sudo().search(domain)

        if taxes:
            for tax in taxes:
                tax.write({'active': False})