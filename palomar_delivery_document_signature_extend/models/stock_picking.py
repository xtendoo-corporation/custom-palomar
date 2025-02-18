from odoo import models, api, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    nif = fields.Char(string='NIF')
    signature = fields.Binary(string='Firma')

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

