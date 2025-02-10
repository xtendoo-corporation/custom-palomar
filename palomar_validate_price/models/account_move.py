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
        return super(account_move, self).button_validate()
