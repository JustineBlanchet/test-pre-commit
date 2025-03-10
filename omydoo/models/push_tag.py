# -*- coding: utf-8 -*-
from odoo import models, fields

class PushTag(models.Model):
    _name = 'push.tag'
    _description = 'Push Tag'

    name = fields.Char('Nom')
    color = fields.Integer('Couleur', default=1)
