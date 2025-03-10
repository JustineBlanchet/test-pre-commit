# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EquipmentOmydoo(models.Model):
    _name = 'equipment.omydoo'
    _description = 'Equipements Omydoo'

    name = fields.Char(string="Nom d'équipement", required=True)
    equipment_category = fields.Many2one('equipment.category', string="Catégorie d'équipement")
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)
    owner_type = fields.Selection([('office', 'Bureau'), ('employee', 'Employé'), ('other', 'Autre'), ('unassigned', 'Non assigné')], required=True)
    owner_user_id = fields.Many2one('hr.employee', string='Employé')
    equipment_location = fields.Many2one('equipment.location', string='Localisation')
    used_other = fields.Char(string='Autre')
    partner_id = fields.Many2one('res.partner', string='Fournisseur')
    model = fields.Char('Modèle', required=True)
    serial_no = fields.Char('Numéro de série', copy=False)
    purchase_date = fields.Date("Date d'achat")
    purchase_price = fields.Float("Prix d'achat")
    warranty_date = fields.Date("Date d'expiration de garantie")
    invoice_id = fields.Many2one('account.move', string='Facture', domain="[('state', '=', 'posted'), ('journal_id.id', '=', '16')]")
    note = fields.Html('Note')
    color = fields.Integer('Color Index')
    out_of_order = fields.Boolean(string='Hors Service', default=False)

class EquipmentCategoryOmydoo(models.Model):
    _name = 'equipment.category'
    _description = 'Equipements Category'

    name = fields.Char("Catégorie d'équipement", required=True)

class EquipmentLocationOmydoo(models.Model):
    _name = 'equipment.location'
    _description = 'Equipements location'

    name = fields.Char("Localisation équipement", required=True)

