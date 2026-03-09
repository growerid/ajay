# -*- coding: utf-8 -*-

from odoo import fields, models, api, _



class ProductTemplate(models.Model):
    _inherit = 'product.template'



    iodine_content_percentage = fields.Float(
        string='Porcentaje de Yodo'
    )