# -*- coding: utf-8 -*-
{
    'name': "Cost Email Alert",

    'summary': """
        Cost Email Alert""",

    'description': """
        Cost Email Alert
    """,

    'author': "VaultOdoo",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/cost_mail.xml',
        'views/views.xml',
        'views/templates.xml',
    ]
}
