from odoo import models, fields, api, _

class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'

    def draft2open(self):
        super(AccountPaymentOrder, self).draft2open()
        for order in self:
            for line in order.payment_line_ids:
                if line.move_line_id:
                    if line.move_line_id.move_id:
                        line.move_line_id.move_id.in_payment_line = True

    def action_cancel(self):
        super(AccountPaymentOrder, self).action_cancel()
        for order in self:
            for line in order.payment_line_ids:
                if line.move_line_id:
                    if line.move_line_id.move_id:
                        line.move_line_id.move_id.in_payment_line = False
