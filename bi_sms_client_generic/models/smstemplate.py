# -*- coding: utf-8 -*-

import time
import urllib

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class email_template(models.Model):
	_inherit = "mail.template"
	
	sms_template = fields.Boolean('SMS Template')
	mobile_to = fields.Char('To (Mobile)', size=256)
	gateway_id = fields.Many2one('sms.smsclient', 'SMS Gateway')


class SmsTemplate(models.Model):
	_name = "sms.message.template"
	
	name = fields.Char(required=True)
	active = fields.Boolean(default=True, required=True)
	sms_message_template = fields.Text('SMS Template', required=True)
