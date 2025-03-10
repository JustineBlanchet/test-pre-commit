from odoo import models, fields, api, _
from datetime import datetime


class ProjectTaskModification(models.Model):
    _name = 'project.task.modification'
    _description = 'Project Task Modification'

    user_id = fields.Many2one('res.users', string='Utilisateur', required=True)
    date = fields.Datetime('Date', default=datetime.now(), required=True)
    reason_id = fields.Many2one('project.task.modification.reason', string='Motif', required=True)
    comment = fields.Char('Commentaire')
    task_id = fields.Many2one('project.task', string='Tâche', required=True)

    @api.model_create_multi
    def create(self, vals):
        ress = super().create(vals)
        for res in ress:
            res.task_id.with_context(request_for_modification=True).write({'stage_id': 678})
        return ress

class ProjectTaskModificationReason(models.Model):
    _name = 'project.task.modification.reason'
    _description = 'Project Task Modification Reason'
    
    name = fields.Char('Motif', required=True)