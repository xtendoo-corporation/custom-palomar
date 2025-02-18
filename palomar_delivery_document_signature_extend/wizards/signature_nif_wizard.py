from odoo import models, fields
import base64

class SignatureNifWizard(models.TransientModel):
    _name = 'signature.nif.wizard'
    _description = 'Wizard para Firma y NIF'

    nif = fields.Char(string='NIF', required=True)
    signature = fields.Binary(string="Firma")


    def action_confirm(self):
        picking = self.env['stock.picking'].browse(self._context.get('active_id'))

        if picking:
            picking.action_assign()

            # Forzar cantidades para validar aunque no haya stock
            for move in picking.move_ids_without_package:
                move.quantity = move.product_uom_qty
            picking.button_validate()

            picking.write({
                'nif': self.nif,
                'signature': self.signature,
            })

            report = self.env['ir.actions.report'].search([
                ('report_name', '=', 'stock.action_report_delivery')
            ], limit=1)

            if report:
                pdf = report.with_context(
                    active_id=picking.id,
                    signature=self.signature,
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
