from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    minimal_quantity = fields.Char(
        string='Cantidad mínima',
    )
