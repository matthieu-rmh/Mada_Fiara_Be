from odoo import models, fields

class Dashboard(models.Model):
    _name = 'dashboard.analytics'
    _description = 'Dashboard Analytics for transaction'

    date_entry = fields.Date(string="Date")
    amount = fields.Float(string="Total Amount")
    entry_type = fields.Selection([('expense', 'Dépense'),
                              ('revenues', 'Revenue')], string="Type")