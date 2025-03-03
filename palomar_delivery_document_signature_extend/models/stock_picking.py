from odoo import models, api, fields
import base64
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    nif = fields.Char(string='NIF')
    signature = fields.Binary(string='Firma')

    @api.depends('signature')
    def _compute_signature_base64(self):
        for record in self:
            if record.signature:
                # Convierte el campo binario 'signature' en base64 solo cuando sea necesario
                record.signature_base64 = base64.b64encode(record.signature).decode('utf-8')
            else:
                record.signature_base64 = False

    signature_base64 = fields.Char(string='Firma Base64', compute='_compute_signature_base64')

    def action_open_signature_nif_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Firma y NIF',
            'res_model': 'signature.nif.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_id': self.id  # Pasa el ID del picking para usarlo en el wizard
            }
        }

