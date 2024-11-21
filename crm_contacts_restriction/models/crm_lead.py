# models.py
from odoo import models, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    partner_id = fields.Many2one(
        'res.partner',
        string='Contact',
        domain=lambda self: self._get_partner_domain()
    )

    def _get_partner_domain(self):
        if self.env.user.has_group('sales_team.group_sale_salesman'):
            return [('user_id', '=', self.env.uid)]
        return (self.company_id and ['|', ('company_id', '=', False),
                                     ('company_id', 'parent_of', [self.company_id])] or ['|',
                                                                                         ('company_id', '=', False), (
                                                                                         'company_id', 'parent_of',
                                                                                         [''])]) + ([])
