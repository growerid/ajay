# -*- coding: utf-8 -*-

from odoo import fields, models, api, _



class ProductCategory(models.Model):
    _inherit = 'product.category'



    iodine_content_percentage = fields.Float(
        string='Porcentaje de Yodo'
    )