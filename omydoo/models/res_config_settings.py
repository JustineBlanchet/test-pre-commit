# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    testing_project_coefficient = fields.Float(string="Pourcentage calcul du temps de tâche Testing / Chefferie de projet", config_parameter='omydoo.testing_project_coefficient', default=0.4)