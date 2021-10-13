# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
	_inherit = 'product.template'

	display_cost_price = fields.Float(string='Display Cost')