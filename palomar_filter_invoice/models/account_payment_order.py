from odoo import models, fields, api, _

class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'

    @api.depends('payment_line_ids')
    def _compute_payment_line(self):
        for order in self:
            for line in order.payment_line_ids:
                line.move_line_id.move_id.in_payment_line = True
                print("*"*50)
                print('line.move_line_id.move_id.in_payment_line', line.move_line_id.move_id.in_payment_line)
