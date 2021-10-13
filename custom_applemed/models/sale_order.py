# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ast import literal_eval

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	# sale new workflow, skipping quotations
	@api.model
	def create(self, vals):
		res = super(SaleOrder, self).create(vals)
		if 'search_default_my_quotation' not in self._context:
			res.action_confirm()
		return res

	state = fields.Selection(selection_add=[
			('under_review', 'Under Review'), ('approve', 'Approved'),
			('reject', 'Rejected')], 
			ondelete={'under_review': 'cascade', 'approve': 'cascade',
			'reject': 'cascade'})

	# under review state
	def first_under_review(self):
		self.state = 'under_review'

	# approved state
	def action_approved(self):
		self.state = 'approve'

	# reject state
	def action_rejected(self):
		self.state = 'reject'

	# reset to draft state
	def reset_to_draft(self):
		self.state = 'draft'

	# print quotation/order
	def action_print(self):
		"""Print quotation report"""
		return self.env.ref('sale.action_report_saleorder').report_action(self)

class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	approval_manager_id = fields.Many2one('res.users', string="Sales Approval Manager")

	@api.model
	def get_values(self):
		"""Get approval_manager_id from settings """
		res = super(ResConfigSettings, self).get_values()
		get_param = self.env['ir.config_parameter'].sudo().get_param
		approval_manager_id = get_param('custom_applemed.approval_manager_id')
		print("=====> :",approval_manager_id)
		if approval_manager_id:
			approval_manager_id = literal_eval(approval_manager_id)
		res.update(
			approval_manager_id = approval_manager_id,
		)
		appr_grp = self.env.ref('custom_applemed.approval_manager_group')
		if approval_manager_id:
			appr_grp.users = [(6,0,[approval_manager_id])]

		return res

	def set_values(self):
		"""Set approval_manager_id from settings """
		res = super(ResConfigSettings, self).set_values()
		param = self.env['ir.config_parameter'].sudo()
		param.set_param('custom_applemed.approval_manager_id', self.approval_manager_id.id)
		return res