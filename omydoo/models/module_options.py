from odoo import models, fields

class ModuleInteressesOptions(models.Model):
    _name = 'module.options'
    _description = 'Options pour les modules intéressés'

    name = fields.Char(string="Nom de l'option")
