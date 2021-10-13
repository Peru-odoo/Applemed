from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import urllib

class SaleOrder(models.Model):
	_inherit = "sale.order"

	def action_confirm(self):
		res = super(SaleOrder, self).action_confirm()
		sms_obj = self.env['sms.smsclient']
		gateway_id = sms_obj.search([('is_sale','=',True)], limit=1)
		if gateway_id and self.partner_id and self.partner_id.mobile:
			gateway = gateway_id
			url = gateway.url
			name = url
			if self.picking_ids:
				text_message = "Delivery order ref #%s against sales order SO# %s is scheduled for so & so date %s." % (self.picking_ids[0].name , self.name, self.date_order)
			else:
				text_message = "Delivery order ref # against sales order SO# %s is scheduled for so & so date %s." % (self.name, self.date_order)
			if gateway.method == 'http':
				prms = {}
				for p in gateway.property_ids:
					 if p.type == 'user':
						 prms[p.name] = p.value
					 elif p.type == 'password':
						 prms[p.name] = p.value
					 elif p.type == 'to':
						 prms[p.name] = res.partner_id.mobile
					 elif p.type == 'sms':
						 prms[p.name] = text_message
					 elif p.type == 'extra':
						 prms[p.name] = p.value
				params = urllib.parse.urlencode(prms)
				name = url + "?" + params

			queue_obj = self.env['sms.smsclient.queue']
			vals = {
				'name': name,
				'gateway_id': gateway.id,
				'state': 'draft',
				'mobile': self.partner_id.mobile,
				'msg': text_message,
				'validity': 0,
				'deferred': 0, 
				'tag': 'Sale Order',
			}
			queue_obj.create(vals)
		return res