from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_report_base_filename(self):
        return 'FACTURA 30920-%s-%s' % (self.name or 'n/a', self.ref or '')

    def _get_correct_filename_report(self, mail_template):
        if mail_template and mail_template.name == 'Factura: Minas Aguas Teñidas':
            return self._get_report_base_filename()
        return self._get_invoice_report_filename()


