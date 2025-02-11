from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    has_payment_order = fields.Boolean(
        string="Has Payment Order",
        compute="_compute_has_payment_order",
        store=True,
    )

    @api.depends('line_ids.payment_id.payment_order_id')
    def _compute_has_payment_order(self):
        for move in self:
            move.has_payment_order = any(
                line.payment_id.payment_order_id for line in move.line_ids
            )

    def _get_report_base_filename(self):
        return 'FACTURA 30920-%s-%s' % (self.name or 'n/a', self.ref or '')

