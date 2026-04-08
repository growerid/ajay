# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


CONTINENT_TABLE = 'CONTINENTE'
COUNTRY_TALBLE = 'PAISES'


class ProductStatisticsCountryAssignWizard(models.TransientModel):
    _name = 'product.statistics.country.assign.wizard'
    _description = 'Asignación País Estadisticas de Producto'



    original_name_destination = fields.Char(
        string='Original Name Destination',
        readonly=True
    )
    group_name_destination = fields.Many2one(
        comodel_name='res.country',
        string='Group Name Destination',
    )
    set_conversion = fields.Boolean(
        string="Generar Conversión",
        default=True,
        help="Si se encuentra activo, se generará la conversión el la tabla correspondiente."
    )
    conversion_table_id = fields.Many2one(
        string='Tabla de Conversión',
        comodel_name='conversion.table',
        default=lambda self: self._get_country_conversion_table(),
        readonly=True,
    )


    # DEFAULT METHODS

    @api.model
    def _get_country_conversion_table(self):
        return self.env['conversion.table'].search([('name','=',COUNTRY_TALBLE)]).id


    # BUTTON METHODS

    def action_assign_country(self):
        product_statistics_ids = self.env['product.statistics'].browse(
            self.env.context.get('product_statistics_ids', [])
            )
        
        continentConversionTable = self.env['conversion.table'].search(
            [('name','=',CONTINENT_TABLE)]
            )

        for statistic in product_statistics_ids:
            statistic.write({'group_name_destination': self.group_name_destination.id,
                            'continent': continentConversionTable._get_conversion(self.group_name_destination.name)})

        if self.set_conversion:
            self._set_conversion()


    def _set_conversion(self):
        conversionTableLine = self.env['conversion.table.line'].search(
            [('conversion_table_id','=',self.conversion_table_id.id),
             ('value_in','=',self.original_name_destination.lower())]
            )
        
        conversion_vals = {'value_in': self.original_name_destination.lower(),
                'value_out': self.group_name_destination.name}

        
        if conversionTableLine:
            conversionTableLine.write(conversion_vals)
        else:
            conversion_vals['conversion_table_id'] = self.conversion_table_id.id
            conversionTableLine.create(conversion_vals)