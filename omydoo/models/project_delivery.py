from odoo import models, fields, api, _
from datetime import date, timedelta
from odoo.exceptions import UserError

class ProjectDeliveryLine(models.Model):
    _inherit = 'project.delivery.line'

    demandeur_ids = fields.Many2many('res.users', related='task_id.demandeur_ids')
    task_id = fields.Many2one('project.task', domain="[('project_id', '=', project_id), ('id', 'not in', project_delivery_tasks), ('stage_id', 'in', [144, 665])]")
    push_tag_ids = fields.Many2many('push.tag', related='task_id.push_tag_ids')
    
    @api.onchange('task_id')
    def _onchange_task_id(self):
        if self.task_id and self.project_id:
            deliveries = self.env['project.delivery'].search([('project_id', '=', self.project_id.id), ('stage', '=', 'scheduled')])
            if deliveries:
                if any(self.task_id.id in delivery.line_ids.task_id.ids for delivery in deliveries):
                    raise UserError('Cette tâche est déjà présente dans une livraison programmée, merci de regrouper les livraisons ou de choisir une autre tâche')

class ProjectDelivery(models.Model):
    _inherit = 'project.delivery'

    patch_notes = fields.Html(string='Patch notes', compute='_compute_patch_notes', store=True, readonly=False)
    customer_notified = fields.Datetime('Client notifié', tracking=True)

    @api.depends('line_ids.task_id', 'line_ids.task_id.cii_field')
    def _compute_patch_notes(self):
        for record in self:
            notes = ''
            for line in record.line_ids:
                if line.task_id.cii_field:
                    notes += "<h4>%s : %s</h4>\n%s\n" %(line.task_id.key_task, line.task_id.name, line.task_id.cii_field)
            record.patch_notes = notes

    def export_patch_note(self):
        return self.env.ref('omydoo.action_report_project_delivery').report_action(self)
