# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, RedirectWarning

from dateutil.relativedelta import relativedelta
import requests
import json



class ProductStatisticsWizard(models.TransientModel):
    _name = 'product.statistics.wizard'
    _description = 'Ejecución Estadisticas de Producto'




    app_id = fields.Many2one(
        comodel_name='product.statistics.app',
        string='App',
        required=True
    )

    date_start = fields.Date(
        string='Fecha Desde',
        default=lambda self: self._get_default_date_start(),
        required=True
    )
    date_end = fields.Date(
        string='Fecha Hasta',
        default=lambda self: self._get_default_date_end(),
        required=True
    )


    @api.model
    def _get_default_date_start(self):
        return fields.Date.context_today(self).replace(day=1)


    @api.model
    def _get_default_date_end(self):
        return fields.Date.context_today(self) + relativedelta(months=1, day=1, days=-1)


    def action_execute(self):
        url = self.env['ir.config_parameter'].sudo().get_param('product_statistics.run_url')
        if not url:
            raise UserError("No se encuentra configurada la URL del Middleware. Revisar parametro 'product_statistics.run_url'")
        
        ps_connection = self.env['product.statistics.connection'].create({
            'app_id': self.app_id.id,
            'exec_date': fields.Datetime.now()
        })

        if not ps_connection:
            raise UserError("No se pudo crear la conexion con el Middleware. Por favor, intente nuevamente en unos segundos.")
        
        json_data = json.dumps({
            'ps_id': ps_connection.id,
            'app_id': self.app_id.id_app,
            'date_start': self.date_start,
            'date_end': self.date_end,
        }, default=str)

        try:
            response = requests.post(url=url, json=json_data)
            if response.status_code != 200:
                raise UserError("Se produjo un error de conexion con el Middleware.\n\nError: %s" % response.text)
        except Exception as e:
            raise UserError("Se produjo un error de conexion con el Middleware.\n\nError: %s" % str(e))
        
        self.env.cr.commit()

        raise RedirectWarning(
            message=_("\nSolicitud enviada correctamente."),
            action={
                'res_model': 'product.statistics.connection',
                'res_id': ps_connection.id,
                'type': 'ir.actions.act_window',
                #'domain': [('id','=',ps_connection.id)],
                'target': 'main',
                'views': [(self.env.ref('grw_product_statistics.product_statistics_connection_view_form').id, 'form')],
            },
            button_text=_("Ver Solicitud"),
        )