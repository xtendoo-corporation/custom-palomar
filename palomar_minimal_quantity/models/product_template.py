from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    minimum_delivery_quantity = fields.Float(string='Cantidad mínima de entrega', digits=(16, 4), default=0)
