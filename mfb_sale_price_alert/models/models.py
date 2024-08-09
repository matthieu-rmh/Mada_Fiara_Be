from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_price_modified = fields.Boolean(string="Is Price Modified", default=False)

    @api.onchange('price_unit')
    def _onchange_price_unit_warning(self):
        if self.price_unit < self.product_id.list_price :
            self.write({
                'is_price_modified': True
            })
            return {
                'warning': {
                'title': _("Attention pour %s", self.product_id.name),
                'message': "Le montant saisissé est inférieur au prix de l'article.",
                }
            }
        else :
            self.write({
                'is_price_modified': False
            })
    
    def _action_sale_price_alert(self) :
        print("hello world")