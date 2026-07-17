from odoo import models, fields, api
from odoo.exceptions import AccessError

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

    def write(self, vals):
        # Verificar si se está intentando modificar el campo user_id
        if 'user_id' in vals:
            # Verificar si el usuario actual tiene permisos para modificar comerciales
            if not self.env.user.has_group('palomar_administration.administrador_comerciales'):
                raise AccessError("No tienes permisos para modificar el campo comercial. Contacta con un administrador de comerciales.")

        return super(ResPartner, self).write(vals)

    @api.model
    def create(self, vals):
        # Verificar si se está intentando asignar el campo user_id al crear
        if 'user_id' in vals and vals['user_id']:
            # Verificar si el usuario actual tiene permisos para asignar comerciales
            if not self.env.user.has_group('palomar_administration.administrador_comerciales'):
                raise AccessError("No tienes permisos para asignar el campo comercial. Contacta con un administrador de comerciales.")

        return super(ResPartner, self).create(vals)
