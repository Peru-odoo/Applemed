# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPicking(models.Model):
	_inherit = 'stock.picking'

	delivery_tag_ids = fields.Many2many('delivery.tag', string='Tags')

class DeliveryTag(models.Model):
	_name = 'delivery.tag'
	_description = 'Delivery Tag'
	_rec_name = 'name'

	name = fields.Char(string='Delivery Tag')

class StockMove(models.Model):
	_inherit = 'stock.move'

	delivery_tag_ids = fields.Many2many('delivery.tag', string='Tags')

	# create delivery tags in stock moves
	@api.model
	def create(self, vals):
		res = super(StockMove, self).create(vals)
		if 'reference' in vals:
			reference = self.env['stock.picking'].search([('name','=',vals['reference'])])
		else:
			reference = self.env['stock.picking'].search([('name','=',self.reference)])
		if reference:
			if reference.delivery_tag_ids:
				tags = []
				for tag in reference.delivery_tag_ids:
					tags.append(tag.id)
				res.delivery_tag_ids = [(6, 0, tags)]
		return res

class StockValuationLayer(models.Model):
	_inherit = 'stock.valuation.layer'

	delivery_tag_ids = fields.Many2many('delivery.tag', string='Tags')

	# create delivery tags in stock valuation layer
	@api.model
	def create(self, vals):
		res = super(StockValuationLayer, self).create(vals)
		if 'stock_move_id' in vals:
			move_id = self.env['stock.move'].search([('id','=',vals['stock_move_id'])])
			reference = self.env['stock.picking'].search([('name','=',move_id.reference)])
		
			if reference:
				if reference.delivery_tag_ids:
					tags = []
					for tag in reference.delivery_tag_ids:
						tags.append(tag.id)
					res.delivery_tag_ids = [(6, 0, tags)]
		return res

class StockScrap(models.Model):
	_inherit = 'stock.scrap'

	delivery_tag_ids = fields.Many2many('delivery.tag', string='Tags')

	# create delivery tags in scrap order
	@api.model
	def create(self, vals):
		res = super(StockScrap, self).create(vals)
		if 'picking_id' in vals:
			reference = self.env['stock.picking'].search([('id','=',vals['picking_id'])])
		
			if reference:
				if reference.delivery_tag_ids:
					tags = []
					for tag in reference.delivery_tag_ids:
						tags.append(tag.id)
					res.delivery_tag_ids = [(6, 0, tags)]
		return res