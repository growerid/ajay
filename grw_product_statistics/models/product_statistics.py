# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ProductStatistics(models.Model):
    _name = 'product.statistics'
    _description = 'Estadisticas de Producto'

    

    name = fields.Char(
        string='Código',
        default=lambda self: self._get_statistic_name(),
        readonly=True
    )
    active = fields.Boolean(
        string='Activo',
        default=True,
    )
    ps_connection_id = fields.Many2one(
        comodel_name='product.statistics.connection',
        string='Conexion',
        readonly=True
    )
    app_id = fields.Many2one(
        related='ps_connection_id.app_id'
    )
    year = fields.Char(
        string='Year',
        readonly=True
    )
    quarter = fields.Char(
        string='Quarter',
        readonly=True
    )
    month = fields.Char(
        string='Month',
        readonly=True
    )
    fob_date = fields.Date(
        string='FOB Date',
        readonly=True
    )
    cif_date = fields.Date(
        string='CIF Date',
        readonly=True
    )
    hs_code_2 = fields.Many2one(
        comodel_name='product.template',
        string='HS Code 2'
    )
    product_group = fields.Many2one(
        related='hs_code_2.categ_id',
        string='Product Group',
    )
    original_name_destination = fields.Char(
        string='Original Name Destination',
        readonly=True
    )
    group_name_destination = fields.Many2one(
        comodel_name='res.country',
        string='Group Name Destination',
        readonly=True
    )
    continent = fields.Selection(
        [('asia_oceania','Asia & Ocenania'),
         ('emea','EMEA'),
         ('latam','LATAM'),
         ('nam','NAM'),
         ('nd','Not Declared')],
         string='Continent',
         readonly=True
    )
    market_zone = fields.Many2one(
        comodel_name='res.country.group',
        string='Market Zone',
        compute='_compute_market_zone'
    )
    origin = fields.Many2one(
        comodel_name='res.country',
        string='Origin',
        readonly=True
    )
    producer = fields.Many2one(
        comodel_name='res.partner',
        string='Producer',
        readonly=True
    )
    cluster = fields.Many2many(
        related='producer.category_id',
        string='Cluster',
        readonly=True
    )
    detail = fields.Char(
        string='Detail',
        readonly=True
    )
    quantity_kg = fields.Float(
        string='Quantity (Kg)',
        readonly=True
    )
    quantity_ie_kg = fields.Float(
        string='Quantity IE (Kg)',
        readonly=True
    )
    quantity_mt = fields.Float(
        string='Quantity (MT)',
        readonly=True
    )
    quantity_ie_mt = fields.Float(
        string='Quantity IE (MT)',
        readonly=True
    )
    total_fob = fields.Float(
        string='Total $ FOB',
        readonly=True
    )
    fob_up_kg = fields.Float(
        string='FOB UP $/kg',
        readonly=True
    )
    cif_up_kg = fields.Float(
        string='CIF UP $/kg',
        readonly=True
    )
    total_cif = fields.Float(
        string='Total $ CIF',
        readonly=True
    )
    description = fields.Text(
        string='Description',
        readonly=True
    )
    hs_source = fields.Text(
        string='HS Source',
        readonly=True
    )
    hs_matched = fields.Text(
        string='HS Matched',
        readonly=True
    )
    needs_llm = fields.Text(
        string='Needs LLM',
        readonly=True
    )
    source = fields.Text(
        string='Source',
        readonly=True
    )
    bill_of_landing = fields.Char(
        string='Bill of Landing',
        readonly=True    
    )



    # COMPUTE METHODS

    @api.depends('group_name_destination')
    def _compute_market_zone(self):
        for record in self:
            record.market_zone = record._get_market_zone()


    # OTHER METHODS

    def _get_statistic_name(self):
        return self.env['ir.sequence'].next_by_code('product.statistics.sequence')


    def _get_market_zone(self):
        return self.group_name_destination.country_group_ids[0] if self.group_name_destination.country_group_ids else False





class ProductStatisticsConnection(models.Model):
    _name = 'product.statistics.connection'
    _description = 'Conexión Estadisticas de Producto'




    name = fields.Char(
        string='Código',
        default=lambda self: self._get_connection_name(),
    )
    app_id = fields.Many2one(
        comodel_name='product.statistics.app',
        string='App',
    )
    exec_date = fields.Datetime(
        string='Fecha/Hora Ejecución'
    )
    state = fields.Selection(
        [('sent','Solicitud Enviada'),
         ('processing','Procesando'),
         ('finalized','Finalizado'),
         ('error','Error')],
         string='Estado',
         default='sent'
    )
    response = fields.Json(
        string='Respuesta'
    )
    ps_statistics_ids = fields.One2many(
        comodel_name='product.statistics',
        inverse_name='ps_connection_id',
        string='Estadisticas'
    )



    def _get_connection_name(self):
        return self.env['ir.sequence'].next_by_code('product.statistics.connection.sequence')





class ProductStatisticsApp(models.Model):
    _name = 'product.statistics.app'
    _description = 'App de Estadisticas de Productos'


    

    name = fields.Char(
        string='Nombre'
    )
    id_app = fields.Char(
        string='ID App'
    )
    excluded_word_ids = fields.Many2many(
        comodel_name='product.statistics.excluded.words',
        string='Palabras Excluidas'
    )
    tariff_position_ids = fields.Many2many(
        comodel_name='product.statistics.tariff.position',
        string='Posiciones Arancelarias'
    )





class ProductStatisticsExcludedWords(models.Model):
    _name = 'product.statistics.excluded.words'
    _description = 'Estadisticas de Producto - Palabras Excluidas'


    name = fields.Char(
        string='Palabra',
        required=True
    )




class ProductStatisticsTariffPosition(models.Model):
    _name = 'product.statistics.tariff.position'
    _description = 'Estadisticas de Producto - Posición Arancelaria'


    name = fields.Char(
        string='Posición Arancelaria',
        required=True
    )