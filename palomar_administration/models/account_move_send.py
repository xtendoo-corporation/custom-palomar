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
            attachment_exists = self.env['ir.attachment'].search([
                ('res_model', '=', 'account.move'),
                ('res_id', '=', move.id),
                ('name', '=', move._get_report_base_filename())
            ])
            if attachment_exists:
                return []
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


    @api.model
    def _process_send_and_print(self, moves, wizard=None, allow_fallback_pdf=False, **kwargs):
        """ Process the moves given their individual configuration set on move.send_and_print_values.
        :param moves: account.move to process
        :param wizard: account.move.send wizard if exists. If not we avoid raising any error.
        :param allow_fallback_pdf:  In case of error when generating the documents for invoices, generate a proforma PDF report instead.
        """
        from_cron = not wizard

        moves_data = {
            move: {
                **(move.send_and_print_values if not wizard else wizard._get_wizard_values()),
                **self._get_mail_move_values(move, wizard),
            }
            for move in moves
        }

        # Generate all invoice documents.
        self._generate_invoice_documents(moves_data, allow_fallback_pdf=allow_fallback_pdf)

        # Manage errors.
        errors = {move: move_data for move, move_data in moves_data.items() if move_data.get('error')}
        if errors:
            self._hook_if_errors(errors, from_cron=from_cron, allow_fallback_pdf=allow_fallback_pdf)

        # Fallback in case of error.
        errors = {move: move_data for move, move_data in moves_data.items() if move_data.get('error')}
        if allow_fallback_pdf and errors:
            self._generate_invoice_fallback_documents(errors)

        # Send mail.
        success = {move: move_data for move, move_data in moves_data.items() if not move_data.get('error')}
        if success:
            self._hook_if_success(success, from_cron=from_cron, allow_fallback_pdf=allow_fallback_pdf)

        # Update send and print values of moves
        for move, move_data in moves_data.items():
            if from_cron and move_data.get('error'):
                move.send_and_print_values = {'error': True}
            else:
                move.send_and_print_values = False

        to_download = {move: move_data for move, move_data in moves_data.items() if move_data.get('download')}
        if to_download:
            attachment_ids = []
            for move, move_data in to_download.items():
                attachment_ids += self._get_invoice_extra_attachments(move).ids or move_data.get(
                    'proforma_pdf_attachment').ids
            if attachment_ids:
                if kwargs.get('bypass_download'):
                    return attachment_ids
                return self._download(attachment_ids, to_download)

        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def _generate_invoice_documents(self, invoices_data, allow_fallback_pdf=False):
        """ Generate the invoice PDF and electronic documents.
        :param allow_fallback_pdf:  In case of error when generating the documents for invoices, generate a
                                    proforma PDF report instead.
        :param invoices_data:   The collected data for invoices so far.
        """
        for invoice, invoice_data in invoices_data.items():
            if self._need_invoice_document(invoice, invoice_data):
                self._hook_invoice_document_before_pdf_report_render(invoice, invoice_data)
                invoice_data['blocking_error'] = invoice_data.get('error') \
                                                 and not (allow_fallback_pdf and invoice_data.get('error_but_continue'))
                invoice_data['error_but_continue'] = allow_fallback_pdf and invoice_data.get('error_but_continue')

        invoices_data_web_service = {
            invoice: invoice_data
            for invoice, invoice_data in invoices_data.items()
            if not invoice_data.get('error')
        }
        if invoices_data_web_service:
            self._call_web_service_before_invoice_pdf_render(invoices_data_web_service)

        invoices_data_pdf = {
            invoice: invoice_data
            for invoice, invoice_data in invoices_data.items()
            if not invoice_data.get('error') or invoice_data.get('error_but_continue')
        }
        for invoice, invoice_data in invoices_data_pdf.items():
            if self._need_invoice_document(invoice, invoice_data) and not invoice_data.get('error'):
                self._prepare_invoice_pdf_report(invoice, invoice_data)
                self._hook_invoice_document_after_pdf_report_render(invoice, invoice_data)

        # Cleanup the error if we don't want to block the regular pdf generation.
        if allow_fallback_pdf:
            invoices_data_pdf_error = {
                invoice: invoice_data
                for invoice, invoice_data in invoices_data.items()
                if invoice_data.get('pdf_attachment_values') and invoice_data.get('error')
            }
            if invoices_data_pdf_error:
                self._hook_if_errors(invoices_data_pdf_error, allow_fallback_pdf=allow_fallback_pdf)

        # Web-service after the PDF generation.
        invoices_data_web_service = {
            invoice: invoice_data
            for invoice, invoice_data in invoices_data.items()
            if not invoice_data.get('error')
        }
        if invoices_data_web_service:
            self._call_web_service_after_invoice_pdf_render(invoices_data_web_service)

        # Create and link the generated documents to the invoice if the web-service didn't failed.
        for invoice, invoice_data in invoices_data_web_service.items():
            if self._need_invoice_document(invoice, invoice_data) and (not invoice_data.get('error') or allow_fallback_pdf):
                self._link_invoice_documents(invoice, invoice_data)

    @api.model
    def _need_invoice_document(self, invoice, invoice_data):
        """ Determine if we need to generate the documents for the invoice passed as parameter.
        :param invoice:         An account.move record.
        :return: True if the PDF / electronic documents must be generated, False otherwise.
        """
        if invoice_data.get('mail_template_id') and "Factura: Minas Aguas Teñidas" in invoice_data.get('mail_template_id').name:
            invoice_name = invoice._get_report_base_filename()
            create_attachment = self.env['ir.attachment'].search([
                ('name', '=', invoice_name),
                ('res_model', '=', 'account.move')
            ])
            if create_attachment:
                if len(create_attachment) > 1:
                    create_attachment = create_attachment[0]
                # invoice.message_main_attachment_id =  create_attachment
                #invoice.invoice_pdf_report_id = create_attachment
            return False
        return not invoice.invoice_pdf_report_id and invoice.state == 'posted'

    @api.model
    def _prepare_invoice_pdf_report(self, invoice, invoice_data):
        """ Prepare the pdf report for the invoice passed as parameter.
        :param invoice:         An account.move record.
        :param invoice_data:    The collected data for the invoice so far.
        """
        if invoice.invoice_pdf_report_id:
            return

        content, _report_format = self.env['ir.actions.report'] \
            .with_company(invoice.company_id) \
            .with_context(from_account_move_send=True) \
            ._render('account.account_invoices', invoice.ids)
        if invoice_data.get('mail_template_id') and "Factura: Minas Aguas Teñidas" in invoice_data.get(
            'mail_template_id').name:
            invoice_data['pdf_attachment_values'] = {
                'raw': content,
                'name': invoice._get_report_base_filename(),
                'mimetype': 'application/pdf',
                'res_model': invoice._name,
                'res_id': invoice.id,
                'res_field': 'invoice_pdf_report_file',  # Binary field
            }
        else:
            invoice_data['pdf_attachment_values'] = {
                'raw': content,
                'name': invoice._get_invoice_report_filename(),
                'mimetype': 'application/pdf',
                'res_model': invoice._name,
                'res_id': invoice.id,
                'res_field': 'invoice_pdf_report_file',  # Binary field
            }


