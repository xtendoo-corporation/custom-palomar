from odoo import models, fields, api
from odoo.exceptions import ValidationError

class account_move(models.Model):
    _inherit = 'account.move'

    def button_validate(self):
        for move in self:
            for line in move.invoice_line_ids:
                if line.price_unit == 0:
                    raise ValidationError(
                        'El precio del producto %s no puede ser 0.' % line.product_id.name
                    )

                # Validar que el precio no sea negativo
                print("*"*80)
                print("line.price_unit:", line.price_unit)
                print("line.purchase_price:", line.purchase_price)

                # Validar que el precio no sea menor que el coste
                if line.price_unit < line.purchase_price:
                    raise ValidationError(
                        'El precio del producto %s (%s) no puede ser inferior a su coste (%s).' % (
                            line.product_id.name,
                            round(line.price_unit, 2),
                            round(line.line.purchase_price, 2)
                        )
                    )
        return super(account_move, self).button_validate()
