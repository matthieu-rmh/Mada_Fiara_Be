from odoo import models, fields
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _action_set_included_tax_to_all_products(self):
        """
        Action to set all products / goods tax to 20 % G INC by default 
        """

        # Fetch only stockable products
        product_items = self.env['product.template'].search([('detailed_type' , '=', 'product')])

        # Get the included tax on_invoice
        inc_tax = self.get_inc_tax()
        
        # Check if any matching tax was found
        if inc_tax:
            # set active to inc_tax
            if inc_tax.active is False:
                inc_tax.write({"active": True})

            for item in product_items:
                item.write({'taxes_id': [(6, 0, [inc_tax.id])]})
        else:
            # Handle the case where no matching tax is found
            _logger.warning("No matching tax found for '20% G INC'")
            # You might want to create the tax here, or skip this record, depending on your requirements


    def get_inc_tax(self):
        """
        Get the included tax on_invoice

        """

        acc = self.env['account.tax'].sudo().search([
            ('tax_group_id', '=', 2),
            ('tax_scope', '=', 'consu'),
            ('type_tax_use', '=', 'sale'),
            ('price_include', '=', True)
            ])
        

        if acc:
            acc = acc[0]
        # Tax won't be found if not active yet
        else:
            acc = self.env['account.tax'].sudo().search([
            ('tax_group_id', '=', 2),
            ('tax_scope', '=', 'consu'),
            ('type_tax_use', '=', 'sale'),
            ('price_include', '=', True),
            ('active', '=', False)
            ])[0]

        # Activate the 20% INC tax (not activated by default)
        if not acc.active:
            acc.write({'active': True})
        
        return acc

        


    

