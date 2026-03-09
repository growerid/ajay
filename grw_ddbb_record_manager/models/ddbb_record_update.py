# -*- coding: utf-8 -*-


from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError
from ast import literal_eval



class DdbbRecordManager(models.TransientModel):
    _name = 'ddbb.record.manager'
    _description = 'DDBB Records Manager'

    name = fields.Char(
        string='Nombre',
        default='DDBB Records Manager'
    )
    type_action = fields.Selection(
        [('write','Actualizar'),
         ('delete','Eliminar')],
         string='Accion',
         required=True,
         default='write'
    )
    data_model = fields.Selection(
        [('sale','Ventas'),
        ('purchase','Compras'),
        ('stock','Inventario'),
        ('accounting','Facturación/Contabilidad'),
        ('payment','Pagos'),
        ('aplicativos','Aplicativos'),
        ('all','Todo')],
        string='Modelo de Datos'
    )
    model_ids = fields.Many2many(
        comodel_name='ir.model',
        string='Modelos'
    )
    model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Modelo'
    )
    model = fields.Char(
        related='model_id.model'
    )
    filter_domain = fields.Char(
        string='Dominio'
    )
    ddbb_manager_field_ids = fields.One2many(
        comodel_name='ddbb.record.manager.field',
        inverse_name='ddbb_manager_id',
        string='Campos'
    )


    @api.onchange('data_model')
    def onchange_data_model(self):
        self.model_ids = [(6, 0, self._get_data_model_models(self.data_model).ids)]

    
    @api.onchange('model_ids')
    def onchange_model_ids(self):
        if len(self.model_ids) == 1:
            self.model_id = self.model_ids[0]
        else:
            self.model_id = False


    # BUTTON METHODS
    def action_write_model_data(self):
        values = {}

        # Se recorren todos los campos cuyo valor no sea un valor referenciado
        for field in self.ddbb_manager_field_ids.filtered(lambda f: f.field_value[:6] != 'record'):
            if field.field.ttype in ['integer','many2one']:
                if str(field.field_value).upper() == 'FALSE':
                    values[field.field.name] = False
                else:
                    values[field.field.name] = int(field.field_value)
            elif field.field.ttype in ['float']:
                values[field.field.name] = float(field.field_value)
            elif field.field.ttype in ['char','text','selection']:
                values[field.field.name] = str(field.field_value)
            elif field.field.ttype in ['many2many','one2many']:
                values[field.field.name] = [(4,int(field.field_value))]
            elif field.field.ttype in ['date']:
                values[field.field.name] = datetime.strptime(str(field.field_value).replace('/','').replace('-',''), '%Y%m%d').date()
            elif field.field.ttype in ['datetime']:
                values[field.field.name] = datetime.strptime(str(field.field_value).replace('/','').replace('-',''), '%Y%m%d')
            elif field.field.ttype in ['boolean']:
                values[field.field.name] = True if field.field_value.upper() == 'TRUE' else False

        # Se obtienen los registos a modificar
        domain = literal_eval(self.filter_domain) if self.filter_domain not in ['', False] else []
        records = self.env[self.model].search(domain)

        if len(values) != 0:
            # Actualizacion valores fijos
            records.write(values)

        # Se preparan los valores de campos con valor referenciado
        for record in records:
            values = {}
            for field in self.ddbb_manager_field_ids.filtered(lambda f: f.field_value[:6] == 'record'):
                values[field.field.name] = eval(str(field.field_value))

            if len(values) != 0:
                # Actualizacion valores referenciados
                record.write(values)

        

    def action_delete_models_data(self):
        if len(self.model_ids) == 0:
            raise UserError("No se seleccionaron modelos para eliminar")
        
        domain = literal_eval(self.filter_domain) if self.filter_domain not in ['', False] else []

        for model in self.model_ids:
            sql_domain = "true"

            # VER DE REEMPLAZAR EL DOMINIO USANDO _where_calc()
            # EJEMPLO: self.env['account.move.line']._where_calc(domain)
            try:
                to_unlink_ids = self.env[model.model].search(domain).ids
            except Exception as e:
                raise UserError("La eliminacion de los datos produjo un error.\nError: %s" % e)
            
            if to_unlink_ids and len(to_unlink_ids) != 0:
                sql_domain = "id in %s" % str(to_unlink_ids).replace('[','(').replace(']',')')

            sql_table = model.model.replace('.','_')
            sql_query = "DELETE FROM %s WHERE %s" % (sql_table, sql_domain)

            try:
                self._cr.execute(sql_query)
                self._cr.commit()
            except Exception as e:
                raise UserError("La eliminacion de los datos produjo un error.\nError: %s" % e)

    

    # OTHER METHODS
    def _get_data_model_models(self, model):
        models_list = []
        if model == 'sale':
            models_list = [
                'sale.order.line',
                'sale.order'
                ]
        elif model == 'purchase':
            models_list = [
                'purchase.order.line',
                'purchase.order',
                'purchase.requisition.line',
                'purchase.requisition'
                ]
        elif model == 'stock':
            models_list = [
                'stock.quant',
                'stock.move.line',
                'stock.package_level',
                'stock.quantity.history',
                'stock.quant.package',
                'stock.move',
                'stock.picking',
                'stock.scrap',
                'stock.picking.batch',
                'stock.inventory.line',
                'stock.inventory',
                'stock.valuation.layer',
                'stock.production.lot',
                'procurement.group',
                ]
        elif model == 'accounting':
            models_list = [
                'account.analytic.line',
                'account.analytic.account',
                'account.partial.reconcile',
                'account.move.line',
                'account.move',
            ]
        elif model == 'payment':
            models_list = [
                'account.bank.statement.line',
                'account.payment.voucher',
                'account.payment',
                'account.payment.retention',
                'account.check',
                'account.check.book',
                'account.check.operation',
            ]
        elif model == 'aplicativos':
             models_list = [
                'account.aplication.export',
                'iva.digital',
            ]
        elif model == 'all':
            models_list = [
                'sale.order.line',
                'sale.order',
                'purchase.order.line',
                'purchase.order',
                'purchase.requisition.line',
                'purchase.requisition',
                'stock.quant',
                'stock.move.line',
                'stock.package_level',
                'stock.quantity.history',
                'stock.quant.package',
                'stock.move',
                'stock.picking',
                'stock.scrap',
                'stock.picking.batch',
                'stock.inventory.line',
                'stock.inventory',
                'stock.valuation.layer',
                'stock.production.lot',
                'procurement.group',
                'account.analytic.line',
                'account.analytic.account',
                'account.partial.reconcile',
                'account.move.line',
                'account.move',
                'account.bank.statement.line',
                'account.payment.voucher',
                'account.payment',
                'account.payment.retention',
                'account.check',
                'account.check.operation',
                'account.check.book',
                ]

        return self.env['ir.model'].search([('model','in',models_list)])


class DdbbRecordManagerField(models.TransientModel):
    _name = 'ddbb.record.manager.field'
    _description = 'DDBB Records Manager Fields'


    ddbb_manager_id = fields.Many2one(
        comodel_name='ddbb.record.manager'
    )
    field = fields.Many2one(
        comodel_name='ir.model.fields',
        string='Campo'
    )
    field_value = fields.Char(
        string='Valor'
    )