from odoo import models, fields
import base64

class SignatureNifWizard(models.TransientModel):
    _name = 'signature.nif.wizard'
    _description = 'Wizard para Firma y NIF'

    nif = fields.Char(string='NIF')
    custom_signature = fields.Binary(string="Firma")

    def action_confirm(self):
        picking = self.env['stock.picking'].browse(self._context.get('active_id'))

        if picking:
            picking.action_assign()

            for move in picking.move_ids_without_package:
                move.quantity = move.product_uom_qty
            picking.button_validate()

            signature_bin = False
            if self.custom_signature:
                try:
                    signature_bin = base64.b64decode(self.custom_signature)
                except Exception as e:
                    raise ValueError(f"Error decoding signature: {e}")

            picking.write({
                'nif': self.nif,
                'signature': signature_bin,
            })

            print(f"Nif: {self.nif}")

            report = self.env['ir.actions.report'].search([
                ('report_name', '=', 'stock.action_report_delivery')
            ], limit=1)

            if report:
                pdf = report.with_context(
                    active_id=picking.id,
                    custom_signature=self.custom_signature,
                    nif=self.nif
                )._render_qweb_pdf([picking.id])[0]

                attachment = self.env['ir.attachment'].create({
                    'name': 'Firma y NIF de la Entrega',
                    'type': 'binary',
                    'datas': base64.b64encode(pdf),
                    'mimetype': 'application/pdf',
                    'res_model': 'stock.picking',
                    'res_id': picking.id,
                })

                picking.message_post(
                    body="Se ha añadido el reporte de firma y NIF.",
                    attachment_ids=[attachment.id]
                )

        return {'type': 'ir.actions.act_window_close'}
