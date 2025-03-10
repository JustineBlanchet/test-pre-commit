from odoo import models

class ReportProjectDelivery(models.AbstractModel):
    _name = 'report.omydoo.project.delivery'

    def _get_report_values(self, docids, data=None):
        docs = self.env['project.delivery'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'project.delivery',
            'docs': docs,
        }