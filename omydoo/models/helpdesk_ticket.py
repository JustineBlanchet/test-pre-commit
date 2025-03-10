# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api

class HelpDeskTicketInherited(models.Model):
    _inherit = 'helpdesk.ticket'

    infos_customer_omydoo = fields.Text(string="Information de l'instance", help="Correspond aux informations de l'instance du client.", compute='_compute_infos_customer_omydoo')

    @api.depends('partner_id')
    def _compute_infos_customer_omydoo(self):
        for record in self:
            customer_infos = ""
            if record.partner_id:
                pid = record.partner_id

                if pid.odoo_hosting_id:
                    customer_infos += "Hébergement: %s" % pid.odoo_hosting_id.name

                if pid.type_eece_omydoo:
                    customer_infos += "\nType: %s" % pid.type_eece_omydoo

                if pid.odoo_version_id:
                    customer_infos += "\nVersion: %s" % pid.odoo_version_id.name
                    
                if not customer_infos:
                    customer_infos = "Veuillez mettre à jour les informations dans le champs contact." 

            record.infos_customer_omydoo = customer_infos

    def subscribe_project_manager(self):
        partner = self.partner_id
        if partner and partner.project_manager_id.id:
            if partner.project_manager_id.id not in self.message_follower_ids.ids:
                self.message_subscribe(partner_ids=[self.partner_id.project_manager_id.id])

    @api.model_create_multi
    def create(self, vals_list):
        res = super(HelpDeskTicketInherited, self).create(vals_list)
        self.subscribe_project_manager()
        return res

    def write(self, vals):
        res = super(HelpDeskTicketInherited, self).write(vals)
        self.subscribe_project_manager()
        return res