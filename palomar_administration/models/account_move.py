from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_report_base_filename(self):
        return 'FACTURA 30920-%s-%s' % (self.name or 'n/a', self.ref or '')


