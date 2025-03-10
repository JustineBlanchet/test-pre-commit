import logging

from odoo import api, fields, models, Command

class FollowupManualReminderInherited(models.TransientModel):
    _inherit = 'account_followup.manual_reminder'

    def process_followup(self):
        action = super(FollowupManualReminderInherited, self).process_followup()
        for invoice in self.partner_id.unpaid_invoice_ids:
            invoice.followup_done = True

        return action