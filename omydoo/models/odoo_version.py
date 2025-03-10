from odoo import fields,models

class OdooVersion(models.Model):
    _name = "odoo.version"
    _description = "Odoo Version"

    name = fields.Char('Nom', required=True)
    color = fields.Integer('Couleur', default=6)
