from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_price_modified = fields.Boolean(string="Is Price Modified", default=False, compute='_compute_price_unit_warning')

    @api.depends('product_id', 'price_unit')
    def _compute_price_unit_warning(self):
        for line in self:
            if line.price_unit < line.product_id.list_price :
                line.is_price_modified = True
                # return {
                #     'warning': {
                #     'title': _("Attention pour %s", line.product_id.name),
                #     'message': "Le montant saisissé est inférieur au prix de l'article.",
                #     }
                # }
            else :
                line.is_price_modified = False
    
    def _action_sale_price_alert(self) :
        print("hello world")