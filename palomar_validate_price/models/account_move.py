from odoo import models, fields, api
from odoo.exceptions import ValidationError

class account_move(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        for move in self:
            for line in move.invoice_line_ids:
                if line.price_unit == 0:
                    raise ValidationError(
                        f'El precio del producto {line.product_id.name} no puede ser 0.'
                    )
                print("*" * 80)
                print("line.price_unit:", line.price_unit)
                print("line.purchase_price:", line.purchase_price)
                if line.price_unit < line.purchase_price:
                    raise ValidationError(
                        f'El precio del producto {line.product_id.name} ({round(line.price_unit, 2)}) no puede ser inferior a su coste ({round(line.purchase_price, 2)}).'
                    )
        return super().action_post()
