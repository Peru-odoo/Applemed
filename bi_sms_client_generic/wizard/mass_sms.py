
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError



class part_sms(models.TransientModel):
    _name = 'part.sms'

    def _default_get_gateway(self):
        if self._context is None:
            self._context = {}
        sms_obj = self.env['sms.smsclient']
        gateway_ids = sms_obj.search( [], limit=1)
        return gateway_ids and gateway_ids[0] or False



    @api.onchange('gateway_id')
    def onchange_gateway_mass(self):
        if context is None:
            context = {}
        if not gateway_id:
            return {}
        sms_obj = self.pool.get('sms.smsclient')
        gateway = sms_obj.browse(self.gateway_id)
        return {
            'value': {
                'validity': gateway.validity, 
                'classes': gateway.classes,
                'deferred': gateway.deferred,
                'priority': gateway.priority,
                'coding': gateway.coding,
                'tag': gateway.tag,
                'nostop': gateway.nostop,
            }
        }

    def _merge_message(self, cr, uid, message, object, partner, context=None):
        def merge(match):
            exp = str(match.group()[2: -2]).strip()
            result = eval(exp, {'object': object, 'partner': partner})
            if result in (None, False):
                return str("--------")
            return str(result)
        com = re.compile('(\[\[.+?\]\])')
        msg = com.sub(merge, message)
        return msg

    def sms_mass_send(self):
        datas = {}
        gateway_id = self.gateway.id
        client_obj = self.env['sms.smsclient']
        partner_obj = self.env['res.partner']
        active_ids = self._context.get('active_ids')
        ctx = self._context
        if ctx.get('active_model') == 'res.partner':
            for data in self:
                if not data.gateway:
                    raise UserError(_('SMS Gateway Not Found...!!!'))
                else:
                    for partner in partner_obj.browse(active_ids):
                        if partner.mobile:
                            data.mobile_to = partner.mobile
                            data.text = data.sms_message_template_id.sms_message_template
                            client_obj.send_msg(data)
        elif ctx.get('active_model'):
            for data in self:
                if not data.gateway:
                    raise UserError(_('SMS Gateway Not Found...!!!'))
                else:
                    model = ctx.get('active_model')
                    order_ids = self.env[model].search([('id','in',active_ids)])
                    partner_ids = order_ids.mapped('partner_id').filtered(lambda x:x.mobile != False)
                    for partner in partner_ids:
                        data.mobile_to = partner.mobile
                        data.text = data.sms_message_template_id.sms_message_template
                        client_obj.send_msg(data)
        return True

    @api.model
    def _get_default_partner(self):
        ctx = self._context
        if ctx.get('active_model') == 'res.partner':
            active_ids = self._context.get('active_ids')
            partners = self.env['res.partner'].search([('id','in',active_ids), ('mobile','!=',False)])
            return partners if partners else False
        elif ctx.get('active_model'):
            active_ids = self._context.get('active_ids')
            model = ctx.get('active_model')
            order_ids = self.env[model].search([('id','in',active_ids)])
            partner_ids = order_ids.mapped('partner_id').filtered(lambda x:x.mobile != False)
            return partner_ids if partner_ids else False

    partner_ids = fields.Many2many("res.partner", readonly="1", default=_get_default_partner)
    gateway = fields.Many2one('sms.smsclient', 'SMS Gateway', required=True, default=_default_get_gateway)
    text  = fields.Text('Text', related="sms_message_template_id.sms_message_template")
    validity  = fields.Integer('Validity',
            help='The maximum time -in minute(s)- before the message is dropped')
    classes1 = fields.Selection([
                ('0', 'Flash'),
                ('1', 'Phone display'),
                ('2', 'SIM'),
                ('3', 'Toolkit'),
            ], 'Class',
            help='The sms class: flash(0),phone display(1),SIM(2),toolkit(3)')
    deferred = fields.Integer('Deferred',
            help='The time -in minute(s)- to wait before sending the message')
    priority = fields.Selection([
                ('0', '0'),
                ('1', '1'),
                ('2', '2'),
                ('3', '3')
            ], 'Priority', help='The priority of the message')
    coding  = fields.Selection([
                ('1', '7 bit'),
                ('2', 'Unicode')
            ], 'Coding', help='The sms coding: 1 for 7 bit or 2 for unicode')
    tag  = fields.Char('Tag', size=256, help='An optional tag')
    nostop1 = fields.Selection([
                ('0', '0'),
                ('1', '1')
            ], 'NoStop',
            help='Do not display STOP clause in the message, this requires that this is not an advertising message')
    sms_message_template_id = fields.Many2one("sms.message.template", string="SMS Template",
        domain=[('active', '=', True)], required=True)
