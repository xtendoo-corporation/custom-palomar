from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.constrains('product_uom_qty')
    def _check_minimal_quantity(self):
        for line in self:
            if line.product_id.minimal_quantity and line.product_uom_qty < float(line.product_id.minimal_quantity):
                raise ValidationError(
                    'La cantidad del producto %s debe ser mayor o igual a la cantidad mínima de %s.' % (
                        line.product_id.name, line.product_id.minimal_quantity)
                )

    @api.constrains('price_unit')
    def _check_price_not_zero(self):
        for line in self:
            if line.price_unit == 0:
                raise ValidationError(
                    'El precio del producto %s no puede ser 0.' % line.product_id.name
                )
