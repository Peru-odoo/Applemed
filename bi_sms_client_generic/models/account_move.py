from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import urllib

class AccountMove(models.Model):
	_inherit = "account.move"

	def action_post(self):
		res = super(AccountMove, self).action_post()
		sms_obj = self.env['sms.smsclient']
		gateway_id = sms_obj.search([('is_invoice','=',True)], limit=1)
		if gateway_id and self.partner_id and self.partner_id.mobile:
			gateway = gateway_id
			url = gateway.url
			name = url
			text_message = "Dear %s, Here is your invoice %s amounting in %s has been generated. Please remit payment at your earliest convenience.- %s" % (
				self.partner_id.name, self.name, round(self.amount_total, 2),
				self.company_id.name)
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