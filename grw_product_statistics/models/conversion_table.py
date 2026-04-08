# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError



class ConversionTable(models.Model):
    _name = 'conversion.table'
    _description = 'Tabla de Conversión'



    name = fields.Char(
        string='Código',
        size=10,
        required=True
    )
    description = fields.Char(
        string='Descripción'
    )
    conversion_line_ids = fields.One2many(
        comodel_name='conversion.table.line',
        inverse_name='conversion_table_id',
        string='Conversiones'
    )


    # CONSTRAINS METHODS

    @api.constrains('name')
    def _control_name(self):
        for table in self:
            if self.search([('name','=',table.name),('id','!=',table.id)]):
                raise UserError("\nYa existe una tabla con el nombre %s." % table.name)
            

    # OTHER METHODS

    def _get_conversion(self, value_in):
        return self.conversion_line_ids.filtered(lambda l: l.value_in.lower() == value_in.lower()).value_out





class ConversionTableLine(models.Model):
    _name = 'conversion.table.line'
    _description = 'Tabla de Conversion - Linea'



    conversion_table_id = fields.Many2one(
        comodel_name='conversion.table',
        string='Tabla de Conversión'
    )
    value_in = fields.Char(
        string='Valor Origen',
        required=True
    )
    value_out = fields.Char(
        string='Valor Destino',
        required=True
    )


    # CONSTRAINS METHODS

    @api.constrains('value_in')
    def _control_name(self):
        for line in self:
            if len(line.conversion_table_id.conversion_line_ids.filtered(lambda l: l.value_in == line.value_in)) > 1:
                raise UserError("\nNo pueden existir dos registros con el mismo Valor Origen (%s) para una misma tabla." % line.value_in)


    