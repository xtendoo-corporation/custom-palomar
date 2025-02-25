from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    in_payment_line = fields.Boolean(
        string='Remesada',
        compute='_compute_in_payment_line',
        store=True
    )

    def _compute_in_payment_line(self):
        for move in self:
            payment_lines = self.env['account.payment.line'].search([
                ('move_line_id.move_id', '=', move.id),
                ('order_id', '!=', False)
            ])
            move.in_payment_line = bool(payment_lines)

    @api.model
    def _recompute_all_in_payment_line(self):
        moves = self.search([])
        moves._compute_in_payment_line()
