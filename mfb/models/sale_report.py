from odoo import models, fields

class SaleReport(models.Model):
    _inherit = 'sale.report'

    date_entry = fields.Datetime(string="Date de saisie")

    def _select(self):
        return super(SaleReport, self)._select() + ", s.date_entry as date_entry"

    def _group_by(self):
        return super(SaleReport, self)._group_by() + ", s.date_entry"