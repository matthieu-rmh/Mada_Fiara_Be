from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class StockMove(models.Model):
    _inherit = 'stock.move'

    categ_value = fields.Char(string="Catégorie de produit", compute='_compute_categ_value')

    @api.depends('product_id')
    def _compute_categ_value(self):
        for rec in self:
            rec.categ_value = rec.product_id.categ_id.name

    