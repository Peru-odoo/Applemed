# -*- coding: utf-8 -*-

{
    "name": "SMS Client",
    "version": "13.0.0.0",
    "depends": ["base","mail", "sale", "purchase", "account"],
    "author": "Vault Odoo",
    'license' : 'LGPL-3',
    'images': ['images/sms.jpeg', 'images/gateway.jpeg', 'images/gateway_access.jpeg','images/client.jpeg','images/send_sms.jpeg'],
    "description": """
SMS Client module provides:
-------------
Sending SMSs very easily, individually or collectively.

*Generalities

OpenERP does not directly generate the SMS you will have to subscribe to an operator with a web interface (Type OVH) or via a URL generation.
If you want to use a 'SMPP Method' you must have to install the library "Soap" which can be installed with: apt-get install python-soappy.
You can find it on https://pypi.python.org/pypi/SOAPpy/
You don't need it if you use a "HTTP Method' to send the SMS.

*Use Multiple Gateways.

The Gateway configuration is performed directly in the configuration menu. For each gateway, you have to fill in the information for your operator.

To validate Gateway, code is send to a mobile phone, when received enter it to confirm SMS account.

This Module was developped by SYLEAM and OpenERP SA in a first place.
Then, it was updated to the 7.0 version by Julius Network Solutions.
    """,
    "website": "",
    "category": "Tools",
    "demo": [],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "views/smsclient_view.xml",
        "views/serveraction_view.xml",
        "views/smsclient_data.xml",
        "wizard/mass_sms_view.xml",
        "views/partner_sms_send_view.xml",
        "views/smstemplate_view.xml",
    ],
    'qweb': ['static/src/xml/pos.xml'],
    "active": False,
    "installable": True,
    "images":['static/description/Banner.png'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
