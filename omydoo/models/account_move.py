# -*- coding: utf-8 -*-
from odoo import models, fields

class AccountMoveInheitedOmydoo(models.Model):
    _inherit = 'account.move'

    followup_done = fields.Boolean(string="Relancé")

    def action_create_equipment(self):
        return {
            'name': 'Nouvel équipement',
            'type': 'ir.actions.act_window',
            'res_model': 'equipment.omydoo',
            'view_mode': 'form',
            'view_id': self.env.ref('omydoo.equipment_view_form_inherited_omydoo').id,
            'views': [(self.env.ref('omydoo.equipment_view_form_inherited_omydoo').id, 'form')],
            'context': {'default_invoice_id':self.id, 'default_partner_id': self.partner_id.id, 'default_purchase_date': self.invoice_date},
            'target': 'new',
        }