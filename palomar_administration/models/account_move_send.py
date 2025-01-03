# -*- coding: utf-8 -*-
from markupsafe import Markup
from werkzeug.urls import url_encode

from odoo import _, api, fields, models, modules, tools, Command
from odoo.exceptions import UserError
from odoo.tools.misc import get_lang


class AccountMoveSend(models.TransientModel):
    _inherit = 'account.move.send'

    def _get_default_mail_attachments_widget(self, move, mail_template):
        if mail_template and mail_template.name == 'Factura: Minas Aguas Teñidas':
            attachments =  self._get_placeholder_mail_template_dynamic_attachments_data(move, mail_template)
            if self.l10n_es_edi_facturae_checkbox_xml:
                attachments.append(self._get_placeholder_mail_attachments_data(move)[1])
            return attachments

        return self._get_placeholder_mail_attachments_data(move) \
            + self._get_placeholder_mail_template_dynamic_attachments_data(move, mail_template) \
            + self._get_invoice_extra_attachments_data(move) \
            + self._get_mail_template_attachments_data(mail_template)

    @api.model
    def _get_placeholder_mail_template_dynamic_attachments_data(self, move, mail_template):
        invoice_template = self.env.ref('account.account_invoices')
        extra_mail_templates = mail_template.report_template_ids - invoice_template
        if mail_template and mail_template.name == 'Factura: Minas Aguas Teñidas':
            filename = move._get_report_base_filename()
            return [
                {
                    'id': f'{filename}',
                    'name': f'{filename}',
                    'mimetype': 'application/pdf',
                    'placeholder': True,
                    'dynamic_report': extra_mail_template.report_name,
                } for extra_mail_template in extra_mail_templates
            ]

        else:
            filename = move._get_invoice_report_filename()
            return [
                {
                    'id': f'placeholder_{extra_mail_template.name.lower()}_{filename}',
                    'name': f'{extra_mail_template.name.lower()}_{filename}',
                    'mimetype': 'application/pdf',
                    'placeholder': True,
                    'dynamic_report': extra_mail_template.report_name,
                } for extra_mail_template in extra_mail_templates
            ]

    @api.depends('mail_template_id')
    def _compute_mail_attachments_widget(self):
        for wizard in self:
            if wizard.mode == 'invoice_single':
                manual_attachments_data = [x for x in wizard.mail_attachments_widget or [] if x.get('manual')]
                wizard.mail_attachments_widget = (
                        wizard._get_default_mail_attachments_widget(wizard.move_ids, wizard.mail_template_id)
                        + manual_attachments_data
                )
            else:
                wizard.mail_attachments_widget = []


