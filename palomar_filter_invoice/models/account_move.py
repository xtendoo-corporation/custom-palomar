from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    in_payment_line = fields.Boolean(
        string='Remesada',
        compute='_compute_in_payment_line',
        store=True
    )

    @api.depends('line_ids.account_id.reconcile', 'line_ids.balance')
    def _compute_in_payment_line(self):
        for move in self:
            debit_total = sum(line.debit for line in move.line_ids)
            credit_total = sum(line.credit for line in move.line_ids)
            if debit_total != credit_total:
                print(
                    _("El movimiento (Borrador de factura %s) no está saldado.\n"
                      "El total de débito es igual a %s y el total de crédito es igual a %s.\n"
                      "Tal vez quiera especificar una cuenta por defecto en el diario \"%s\" para saldar cada movimiento de forma automática.") %
                    (move.name, debit_total, credit_total, move.journal_id.name)
                )
                move.in_payment_line = False
                continue

            payment_lines = self.env['account.payment.line'].search([
                ('move_line_id.move_id.id', '=', move.id),
            ])
            move.in_payment_line = bool(payment_lines)

    @api.model
    def _recompute_all_in_payment_line(self):
        moves = self.search([])
        moves._compute_in_payment_line()
