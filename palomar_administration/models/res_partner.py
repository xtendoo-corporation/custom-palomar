from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    user_has_group = fields.Boolean(
        string='User Has Group',
        compute='_compute_user_has_group',
        store=False
    )

    @api.depends('user_id')
    def _compute_user_has_group(self):
        for order in self:
            order.user_has_group = self.env.user.has_group('palomar_administration.change_list_prices')
