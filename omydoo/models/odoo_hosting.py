from odoo import fields,models

class OdooHosting(models.Model):
    _name = "odoo.hosting"
    _description = "Odoo Hosting"

    name = fields.Char('Nom', required=True)
    color = fields.Integer('Couleur', default=6)
