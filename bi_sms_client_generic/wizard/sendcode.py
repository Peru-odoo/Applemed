

from odoo.osv import fields, orm
from odoo.tools.translate import _

class sendcode(orm.TransientModel):
    _name = 'sms.smsclient.code.send'

    def send_code(self, cr, uid, data, context):
        key = md5(time.strftime('%Y-%m-%d %H:%M:%S') + data['form']['smsto']).hexdigest()
        sms_pool = pooler.get_pool(cr.dbname).get('sms.smsclient')
        gate = sms_pool.browse(cr, uid, data['id'])
        msg = key[0:6]
        sms_pool._send_message(cr, uid, data['id'], data['form']['smsto'], msg)
        if not gate.state in('new', 'waiting'):
            raise osv.except_osv(_('Error'), _('Verification Failed. Please check the Server Configuration!'))

        pooler.get_pool(cr.dbname).get('sms.smsclient').write(cr, uid, [data['id']], {'state': 'waiting', 'code': msg})
        return {}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
