from odoo import models, fields, api
from odoo.exceptions import ValidationError

class account_move(models.Model):
    _inherit = 'account.move'


    def action_post(self):
        for move in self:
            print(f'Validando precios de productos en la factura {move.name}...')
            for line in move.invoice_line_ids.filtered(lambda l: l.display_type == 'product'):  # Excluir notas y secciones
                print(f'Validando producto: {line.product_id.name} con precio unitario: {line.price_unit} y coste de compra: {line.purchase_price}')
                if line.price_unit == 0.00:
                    raise ValidationError(
                        f'El precio del producto {line.product_id.name} no puede ser 0.00. Por favor, revisa el producto y corrige su precio.'
                    )
                if line.price_unit < line.purchase_price:
                    raise ValidationError(
                        f'El precio del producto {line.product_id.name} ({round(line.price_unit, 2)}) no puede ser inferior a su coste ({round(line.purchase_price, 2)}).'
                    )
        return super().action_post()
