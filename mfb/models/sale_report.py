from odoo import models, fields

class SaleReport(models.Model):
    _inherit = 'sale.report'

    date_entry = fields.Datetime(string="Date de saisie", readonly=True)

    def _select(self):
        return super()._select() + ", s.date_entry as date_entry"

    def _group_by(self):
        return super()._group_by() + ", s.date_entry"