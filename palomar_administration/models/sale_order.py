from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    user_has_group = fields.Boolean(
        string='User Has Group',
        compute='_compute_user_has_group',
        store=False
    )

    @api.depends('user_id')
    def _compute_user_has_group(self):
        for order in self:
            order.user_has_group = self.env.user.has_group('palomar_administration.change_list_prices')

    def _get_order_lines_to_report(self):
        down_payment_lines = self.order_line.filtered(lambda line:
                                                      line.is_downpayment
                                                      and not line.display_type
                                                      and not line._get_downpayment_state()
                                                      and line.product_uom_qty != 0
                                                      )

        def show_line(line):
            if not line.is_downpayment and line.product_uom_qty != 0:
                return True
            elif line.display_type and down_payment_lines:
                return True  # Only show the down payment section if down payments were posted
            elif line in down_payment_lines:
                return True  # Only show posted down payments
            else:
                return False

        return self.order_line.filtered(show_line)
