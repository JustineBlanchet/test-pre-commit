from odoo import models, fields


class HelpdeskSLA(models.Model):
    _inherit = 'helpdesk.sla'  

    def _default_color(self):
        color = {'Privilège': 4,
                 'Intégral': 10,
                 'Essentiel +': 3,
                 'Essentiel': 1,
                }


        for elem in self:
            elem.sla_def_col = color.get(elem.name, 0)

                
    sla_def_col = fields.Integer(string='SLA Default Color', compute='_default_color')

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    sla_ids_tag = fields.Many2many('helpdesk.sla', related='partner_id.sla_ids', string='SLA Policies Tag')
    sla_def_col = fields.Integer(string='SLA Default Color', compute='_default_color')  

    def _default_color(self):
        color = {'Privilège': 4,
                 'Intégral': 10,
                 'Essentiel +': 3,
                 'Essentiel': 1,
                }


        for elem in self:
            elem.sla_def_col = color.get(elem.name, 0)
