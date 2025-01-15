# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date

class ResUsers(models.Model):
	_inherit = 'res.users'

	customer_amount_target = fields.Float(string="Montant objectif")
