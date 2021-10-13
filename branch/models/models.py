# -*- coding: utf-8 -*-

from odoo import models, fields, api

# branch in users
class ResUsers(models.Model):
	_inherit = 'res.users'

	branch_id = fields.Many2one('branch.master', string='Default Branch', 
		help='The default branch for this user.')
	branch_ids = fields.Many2many('branch.master', 
		string='Allowed Branches')

# branch master
class BranchMaster(models.Model):
	_name = 'branch.master'
	_description = 'Branch Master'

	name = fields.Char(string="Name")
	logo = fields.Binary(string="Branch Logo", readonly=False)
	street = fields.Char()
	street2 = fields.Char()
	zip = fields.Char()
	city = fields.Char()
	state_id = fields.Many2one(
		'res.country.state', 
		string="Fed. State", domain="[('country_id', '=?', country_id)]"
	)
	country_id = fields.Many2one('res.country', string="Country")
	phone = fields.Char(string='Phone', readonly=False)
	mobile = fields.Char(string='Mobile', readonly=False)
	email = fields.Char(string='Email', readonly=False)
	website = fields.Char(readonly=False)
	vat = fields.Char(string="Tax", readonly=False)
	warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse")
	analytic_account_id = fields.Many2one('account.analytic.account', 
						string="Analytic Account")
	branch_registry = fields.Char(string="Branch Registry", readonly=False)
	currency_id = fields.Many2one('res.currency', string='Currency')
	company_id = fields.Many2one('res.company', string='Company')
	header = fields.Binary(string="Header", readonly=False)
	footer = fields.Binary(string="Footer", readonly=False)

# branch in sales
class SaleOrder(models.Model):
	_inherit = 'sale.order'

	branch_id = fields.Many2one('branch.master', string="Branch", 
						default=lambda self: self.get_default_branch(), 
						domain=lambda self: self.get_allowd_branches())
	analytic_account_id = fields.Many2one('account.analytic.account', 
										string="Analytic Account", store=True)
	warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse", store=True)
	# branch_id = fields.Many2one('branch.master', string="Branch", 
	# 					)

	# get default branch of user
	@api.model
	def get_default_branch(self):
		user_id = self.env.user
		default_branch = user_id.branch_id
		if default_branch:
			return default_branch
		else:
			return False

	# get allowed branches of user
	def get_allowd_branches(self):
		user_id = self.env.user
		allowed_branches = user_id.branch_ids
		if allowed_branches:
			return [('id', 'in', allowed_branches.ids)]
		else:
			return [('id', 'in', [])]

	# auto get branch details
	@api.onchange('branch_id')
	def get_related_details_so(self):
		for rec in self:
			if rec.branch_id:
				rec.analytic_account_id = rec.branch_id.analytic_account_id.id
				rec.warehouse_id = rec.branch_id.warehouse_id.id

# branch in purchase
class PurchaseOrder(models.Model):
	_inherit = 'purchase.order'

	branch_id = fields.Many2one('branch.master', string="Branch", 
						default=lambda self: self.get_default_branch(), 
						domain=lambda self: self.get_allowd_branches())
	# branch_id = fields.Many2one('branch.master', string="Branch", 
	# 					)
	analytic_account_id = fields.Many2one('account.analytic.account', 
										string="Analytic Account", store=True)
	warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse", store=True)

	# get default branch of user
	@api.model
	def get_default_branch(self):
		user_id = self.env.user
		default_branch = user_id.branch_id
		if default_branch:
			return default_branch
		else:
			return False

	# get allowed branches of user
	def get_allowd_branches(self):
		user_id = self.env.user
		allowed_branches = user_id.branch_ids
		if allowed_branches:
			return [('id', 'in', allowed_branches.ids)]
		else:
			return [('id', 'in', [])]

	# auto get branch details
	@api.onchange('branch_id')
	def get_related_details_po(self):
		for rec in self:
			if rec.branch_id:
				rec.analytic_account_id = rec.branch_id.analytic_account_id.id
				rec.warehouse_id = rec.branch_id.warehouse_id.id

# branch in invoices/bills
class AccountMove(models.Model):
	_inherit = 'account.move'

	# branch_id = fields.Many2one('branch.master', string="Branch", 
	# 					)
	branch_id = fields.Many2one('branch.master', string="Branch", 
						default=lambda self: self.get_default_branch(), 
						domain=lambda self: self.get_allowd_branches())
	analytic_account_id = fields.Many2one('account.analytic.account', 
										string="Analytic Account", store=True)
	warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse", store=True)

	# auto get branch details
	@api.onchange('branch_id')
	def get_related_details_acc(self):
		for rec in self:
			if rec.branch_id:
				rec.analytic_account_id = rec.branch_id.analytic_account_id.id
				rec.warehouse_id = rec.branch_id.warehouse_id.id

	# get default branch of user
	@api.model
	def get_default_branch(self):
		user_id = self.env.user
		default_branch = user_id.branch_id
		if default_branch:
			return default_branch
		else:
			return False

	# get allowed branches of user
	def get_allowd_branches(self):
		user_id = self.env.user
		allowed_branches = user_id.branch_ids
		if allowed_branches:
			return [('id', 'in', allowed_branches.ids)]
		else:
			return [('id', 'in', [])]

	# auto get branch_id (when generate inv/bill from sales/purchase)
	@api.model
	def create(self, vals):
		res = super(AccountMove, self).create(vals)
		if 'invoice_origin' in vals:
			if vals['invoice_origin'] != False:
				# so invoice
				if vals['move_type'] == 'out_invoice':
					so = self.env['sale.order'].search([
					('name','=',vals['invoice_origin'])])
					branch_id = so.branch_id
					if branch_id:
						res.branch_id = branch_id.id
						res.analytic_account_id = branch_id.analytic_account_id.id
						res.warehouse_id = branch_id.warehouse_id.id
				# po bills
				if vals['move_type'] == 'in_invoice':
					po = self.env['purchase.order'].search([
					('name','=',vals['invoice_origin'])])
					branch_id = po.branch_id
					if branch_id:
						res.branch_id = branch_id.id
						res.analytic_account_id = branch_id.analytic_account_id.id
						res.warehouse_id = branch_id.warehouse_id.id
		return res

class AccountMoveLine(models.Model):
	_inherit = "account.move.line"

	analytic_account_id = fields.Many2one('account.analytic.account', 
						string="Analytic Account",
						related="move_id.analytic_account_id")

class SaleReport(models.Model):
	_inherit = "sale.report"

	branch_id = fields.Many2one('branch.master')

	# add branch in pivot view
	def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
		fields['branch_id'] = ", s.branch_id as branch_id"
		groupby += ', s.branch_id'
		return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)

class AccountInvoiceReport(models.Model):
	_inherit = 'account.invoice.report'

	branch_id = fields.Many2one('branch.master')

	# add branch in pivot view
	def _select(self):
		return super(AccountInvoiceReport, self)._select() + ", move.branch_id as branch_id"

class PurchaseReport(models.Model):
	_inherit = "purchase.report"

	branch_id = fields.Many2one('branch.master')

	# add branch in pivot view
	def _select(self):
		return super(PurchaseReport, self)._select() + ", po.branch_id as branch_id"

	def _group_by(self):
		return super(PurchaseReport, self)._group_by() + ", po.branch_id"