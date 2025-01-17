from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    name_minas = fields.Char('Name minas', compute='_get_report_base_filename_mail', store=True)

    @api.depends('name', 'ref')  # Especifica los campos de los que depende
    def _get_report_base_filename_mail(self):
        for record in self:
            name = record.name.replace("/", "_") if record.name else ""
            record.name_minas = 'FACTURA 30920-%s-%s' % (name, record.ref or '')

    def _get_report_base_filename(self):
        name = ""
        if self.name:
            name = self.name.replace("/", "_")
        return 'FACTURA 30920-%s-%s' % (name or '', self.ref or '')

    def _get_correct_filename_report(self, mail_template):
        if mail_template and mail_template.name == 'Factura: Minas Aguas Teñidas':
            return self._get_report_base_filename()
        return self._get_invoice_report_filename()


