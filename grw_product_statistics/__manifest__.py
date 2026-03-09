# -*- coding: utf-8 -*-
{
    'name': "GRW - Product Statistics",

    'summary': """
        Modulo para Gestión de Estadisticas de Producto """,

    'description': """
        Modulo para Gestión de Estadisticas de Producto
    """,

    'author': "Grower ID",
    'website': "https://www.growerid.com.ar",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Hidden',
    'version': '1.0',
    "license": "AGPL-3",

    'installable': True,
    'auto_install': False,

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    'data': [
        'security/ir.model.access.csv',
        'views/product_statistics_views.xml',
        'views/product_views.xml',
        'views/partner_views.xml',
        'views/product_template_views.xml',
        'views/product_category_views.xml',
        'views/conversion_table_view.xml',
        'wizards/product_statistics_wizards.xml',
        'data/product_statistics_data.xml',
    ],
}