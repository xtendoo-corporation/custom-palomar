from odoo import models, api, fields
import base64
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    nif = fields.Char(string='NIF')
    signature = fields.Binary(string='Firma')
