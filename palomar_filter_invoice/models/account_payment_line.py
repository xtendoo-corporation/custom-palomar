from odoo import models, fields, api, _

class AccountPaymentLine(models.Model):
    _inherit = 'account.payment.line'

    @api.onchange('order_id')
    def _onchange_order_id(self):
        if self.order_id:
            print("/" * 50)
            print('order', self.order_id)
            print('payment_line_ids:', self.order_id.payment_line_ids)
            for line in self.order_id.payment_line_ids:
                print('line:', line)
                if line.move_line_id:
                    print('move_line_id:', line.move_line_id)
                    if line.move_line_id.move_id:
                        line.move_line_id.move_id.in_payment_line = True
                        print("/" * 50)
                        print('line.move_line_id.move_id.in_payment_line', line.move_line_id.move_id.in_payment_line)
                    else:
                        print('move_line_id.move_id is None')
                else:
                    print('move_line_id is None')
