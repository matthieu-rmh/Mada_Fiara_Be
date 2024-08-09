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
            return {
                'warning': {
                'title': _("Attention pour %s", self.product_id.name),
                'message': "Le montant saisissé est inférieur au prix de l'article.",
                }
            }
    
    def _action_sale_price_alert(self) :
        print("hello world")

    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        
        if  res.product_id and res.price_unit < res.product_id.list_price:
            res.is_price_modified = True

        return res

    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        
        for line in self:
            if 'price_unit' in vals and line.product_id:
                if line.price_unit < line.product_id.list_price:
                    line.is_price_modified = True
                else:
                    line.is_price_modified = False

        return res