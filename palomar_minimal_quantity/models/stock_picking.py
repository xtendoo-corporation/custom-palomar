from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        for picking in self:
            for move in picking.move_lines:
                if move.product_id.minimum_delivery_quantity and move.product_uom_qty < move.product_id.minimum_delivery_quantity:
                    raise ValidationError(
                        'La cantidad del producto %s debe ser mayor o igual a la cantidad mínima de %s.' % (
                            move.product_id.name, move.product_id.minimum_delivery_quantity)
                    )
        return super(StockPicking, self).button_validate()
