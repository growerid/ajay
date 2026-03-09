# -*- coding: utf-8 -*-


from odoo import http
from werkzeug.exceptions import NotFound



class Database(http.Controller):



    @http.route('/web/database/manager', type='http', auth="none")
    def manager(self, **kw):
        raise NotFound()


    @http.route('/web/database/selector', type='http', auth="none")
    def manager(self, **kw):
        raise NotFound()