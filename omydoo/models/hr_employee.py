# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrEmployeeInheritedOmydoo(models.Model):
    _inherit = 'hr.employee'

    equipment_count = fields.Integer(string="Equipements", compute="_compute_equipment_count_omydoo")
    github = fields.Char(string='GitHub')

    def _compute_equipment_count_omydoo(self):
        for record in self:
            record.equipment_count = self.env['equipment.omydoo'].search_count([('owner_user_id', '=', record.id)])

    def action_open_employee_equipments(self):
        return {
            'name': 'Equipements',
            'type': 'ir.actions.act_window',
            'res_model': 'equipment.omydoo',
            'view_mode': 'tree',
            'view_id': self.env.ref('omydoo.omd_equipment_view_tree').id,
            'views': [(self.env.ref('omydoo.omd_equipment_view_tree').id, 'tree')],
            'domain': [('owner_user_id', '=', self.id)],
            'context': {'create': False},
        }

    taille_haut = [
        ("xs", "XS"),
        ("s", "S"),
        ("m", "M"),
        ("l", "L"),
        ("xl", "XL"),
        ("xxl", "XXL")
    ]

    pointure = [
        ("34", "34"), ("35", "35"), ("36", "36"), ("37", "37"), ("38", "38"), ("39", "39"),
        ("40", "40"), ("41", "41"), ("42", "42"), ("43", "43"), ("44", "44"), ("45", "45"), ("46", "46"),
    ]

    # Mensurations
    omydoo_tour_poitrine = fields.Integer(string="Tour de poitrine", help="Correspond au tour de poitrine de l'employé(e).", default=000)
    omydoo_longueur_buste = fields.Integer(string="Longueur de buste", help="Correspond à la longueur de buste de l'employé(e).", default=000)
    omydoo_taille_haut = fields.Selection(taille_haut, string="Taille de haut", help="La taille européenne de haut de l'employé(e).")
    omydoo_pointure = fields.Selection(pointure, string="Pointure", help="Correspond à la pointure de l'employé(e).")

    #constraint
    @api.constrains('omydoo_tour_poitrine', 'omydoo_longueur_buste')
    def _check_number(self):
        omydoo_tour_poitrine = self.omydoo_tour_poitrine
        omydoo_longueur_buste = self.omydoo_longueur_buste
        if omydoo_tour_poitrine and len(str(abs(omydoo_tour_poitrine))) > 3:
            raise ValidationError(('Ne peut pas excéder 3 chiffres'))           
        if omydoo_longueur_buste and len(str(abs(omydoo_longueur_buste))) > 3:
            raise ValidationError(('Ne peut pas excéder 3 chiffres'))

class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    github = fields.Char(string='GitHub')
    omydoo_tour_poitrine = fields.Integer(string="Tour de poitrine",
                                          help="Correspond au tour de poitrine de l'employé(e).", default=000)
    omydoo_longueur_buste = fields.Integer(string="Longueur de buste",
                                           help="Correspond à la longueur de buste de l'employé(e).", default=000)
    taille_haut = [
        ("xs", "XS"),
        ("s", "S"),
        ("m", "M"),
        ("l", "L"),
        ("xl", "XL"),
        ("xxl", "XXL")
    ]

    pointure = [
        ("34", "34"), ("35", "35"), ("36", "36"), ("37", "37"), ("38", "38"), ("39", "39"),
        ("40", "40"), ("41", "41"), ("42", "42"), ("43", "43"), ("44", "44"), ("45", "45"), ("46", "46"),
    ]
    omydoo_taille_haut = fields.Selection(taille_haut, string="Taille de haut",
                                          help="La taille européenne de haut de l'employé(e).")
    omydoo_pointure = fields.Selection(pointure, string="Pointure", help="Correspond à la pointure de l'employé(e).")
