# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartnerInherited(models.Model):
    _inherit = 'res.partner'

    hebergement_omydoo_methods = [
        ("odoo_sh", "Odoo Sh"),
        ("nach_it", "Nach It"),
        ("onpremise", "Onpremise"),
        ("odoo_online", "Odoo Online"),
        ("h8l", "H8lio")
    ]

    version_omydoo_methods = [
        ("v13", "V13"),
        ("v14", "V14"),
        ("v15", "V15"),
        ("v16", "V16"),
        ("v17", "V17")
    ]

    type_omydoo_methods = [
        ("community", "Community"),
        ("enterprise", "Enterprise")
    ]


    FOLLOW_PARTNER_FIELDS = ['odoo_hosting_id', 'odoo_version_id', 'type_eece_omydoo', 'project_manager_id']

    # Informations
    hebergement_omydoo = fields.Selection(hebergement_omydoo_methods, string="Hébergement", help="Correspond à l'hébergement de l'instance du client.")
    odoo_hosting_id = fields.Many2one('odoo.hosting', string='Hébergement', help="Hébergement de l'instance client")
    backup_status = fields.Boolean(string="Backup")
    version_omydoo = fields.Selection(version_omydoo_methods ,string="Version", help="Correspond à la version d'odoo du client.")
    odoo_version_id = fields.Many2one('odoo.version', string='Version Odoo')
    type_eece_omydoo = fields.Selection(type_omydoo_methods ,string="Type", help="Correspond au type d'odoo du client.")
    nbu_instance_omydoo = fields.Integer(string="Nombre d'utilisateur", help="Correspond au nombre d'utilisateur de l'instance du client.", default=0)
    lien_instance_omydoo = fields.Char(string="Lien", help="Correspond au lien de l'instance du client.")
    lien_preprod = fields.Char(string="Preprod", help="Correspond au lien de la preprod du client.")
    apps_ids = fields.Many2many('omydoo.apps', string="Applications Externes", help="Correspond aux applications externes liées à l'instance du client.")
    project_manager_id = fields.Many2one('res.partner', string="Project Manager", help="Nom du project manager",
                                         domain="[('is_project_manager', '=', True)]")
    production_date = fields.Date(string='Mise en production le', help='Date de la production')
    date_cloture = fields.Date(string='Date de clôture le', help='Date de fermeture')
    derniere_upgrade = fields.Date(string='Date dernière Upgrade le', help='Dernière montée de version')
    commentaire = fields.Text(string='Commentaires')
    license_ee_omydoo = fields.Char(string="Licence",help="Correspond à la licence d'odoo entreprise du client.")

    # Database
    user_db_omydoo = fields.Char(string="Utilisateur BD", help="Correspond à l'username de la base de données de l'instance.")
    passwd_db_omydoo = fields.Char(string="Mot de passe BD", help="Correspond au mot de passe de la base de données de l'instance.")
    port_db_omydoo = fields.Integer(string="Port", help="Correspond au port de la base de données de l'instance.", default=0000)
    ip_db_omydoo = fields.Char(string="IP", help="Correspond à l'adresse IP de la base de données de l'instance.")

    omydoo_material_ids = fields.One2many('omydoo.material', 'res_partner_id')
    sla_ids_tag = fields.Many2many('helpdesk.sla', related='sla_ids', string='SLA Policies Tag')

    is_project_manager = fields.Boolean("Est un chef de projet")

    @api.constrains('port_db_omydoo')
    def _check_number(self):
        for record in self:
            port_db_omydoo = record.port_db_omydoo
            if port_db_omydoo and len(str(abs(port_db_omydoo))) > 5:
                raise ValidationError(('Ne peut pas excéder 5 chiffres'))

    visibility_license_ee_omydoo = fields.Boolean(default=False, store=False)
    visibility_user_db_omydoo = fields.Boolean(default=False, store=False)
    visibility_passwd_db_omydoo = fields.Boolean(default=False, store=False)

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, subtype_xmlid=None, **kwargs):
        # ID of the user who will send follow-up, idk if necessary to make it configurable
        accountant_user_id = 49
        message = super(ResPartnerInherited, self).message_post(**kwargs)
        if not subtype_xmlid or subtype_xmlid == "mail.mt_comment":
            if self.env.context['uid'] is accountant_user_id:
                for invoice in self.unpaid_invoice_ids:
                    invoice.followup_done = True
        return message

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('parent_id') and not vals.get('is_company'):
                parent = self.env['res.partner'].search([('id', '=', vals.get('parent_id'))],
                                                        limit=1)
                if parent:
                    for field in parent.fields_get():
                        if field in self.FOLLOW_PARTNER_FIELDS and not vals.get(field) and parent[field]:
                            value = parent[field]
                            if not isinstance(value, (str, int, float, list)):
                                if value.id:
                                    value = value.id
                            vals[field] = value

        return super().create(vals_list)

    def write(self, vals):
        for record in self:
            if record.company_type == 'company':
                for field in vals.keys():
                    if field in self.FOLLOW_PARTNER_FIELDS:
                        value = vals[field]
                        if not isinstance(value, (str, int, float, list)):
                            if value.id:
                                value = value.id
                        self.env['res.partner'].browse(record.child_ids.ids)[field] = value

        return super().write(vals)