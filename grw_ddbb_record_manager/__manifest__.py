# -*- coding: utf-8 -*-
{
    'name': "GRW - DDBB Record Manager",

    'summary': """
        GRW - DDBB Record Manager""",

    'description': """
        GRW - DDBB Record Manager
    """,

    'author': "Grower ID",
    'website': "https://www.growerid.com.ar",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.1',
    "license": "AGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/ddbb_record_manager_view.xml',
    ],
}
