# -*- coding: utf-8 -*-
{
    'name': "Custom Applemed",

    'summary': """
        Add Display Cost for products""",

    'description': """
        Add Display Cost for products
    """,

    'author': "VaultOdoo",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'sale_management', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'report/quotation.xml',
        'views/product_cost.xml',
        'views/stock_picking.xml',
        'views/delivery_tag.xml',
        'views/sale_order.xml',
    ]
}
