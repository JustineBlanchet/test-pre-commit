# -*- coding: utf-8 -*-

from odoo import models, fields, api
from random import randint

class OmydooApps(models.Model):
    _name = 'omydoo.apps'
    _description = 'Omydoo Tags for external apps'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Application', required=True)
    color = fields.Integer('Color', default=_get_default_color)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]