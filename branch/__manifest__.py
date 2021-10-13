# -*- coding: utf-8 -*-
{
    'name': "Branch",

    'summary': """
        Branch Master""",

    'description': """
        Branch Master
    """,

    'author': "VaultOdoo",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'purchase', 'pass_analytic_acc_in_journal_app', 'stock', 'custom_applemed'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/sale_order.xml',
        'views/purchase_order.xml',
        'views/customer_invoice.xml',
        'views/res_users.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
