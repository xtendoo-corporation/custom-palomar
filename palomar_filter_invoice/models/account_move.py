from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    in_payment_line = fields.Boolean(
        string='Remesada',
        compute='_compute_in_payment_line',
        store=True
    )

    @api.depends('line_ids')
    def _compute_in_payment_line(self):
        for move in self:
            move.in_payment_line = any(
                self.env['account.payment.line'].search([('move_line_id.move_id', '=', move.id)])
            )
