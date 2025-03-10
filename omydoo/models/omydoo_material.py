# -*- coding: utf-8 -*-
from odoo import models, fields, api

class OmydooMaterial(models.Model):
    _name = 'omydoo.material'
    _description = 'Omydoo Material'

    brand = fields.Char(string='Marque')
    model = fields.Char(string='Modèle')
    serial_number = fields.Char(string='N° de série')
    install_date = fields.Date(string='Date d\'installation')
    waranty_expiration_date = fields.Date(string='Date de fin de garantie')
    res_partner_id = fields.Many2one('res.partner', string='Client')
