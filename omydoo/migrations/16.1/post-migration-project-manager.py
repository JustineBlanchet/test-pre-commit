from odoo import api, SUPERUSER_ID
import logging
def migrate(cr, version):
    # Set project manager directly when migrating
    cr.execute("UPDATE res_partner rp SET is_project_manager = TRUE WHERE rp.id IN (3, 7, 1344, 3926)")

    # propagate data from old project_manager (selection of string) field to new project_manager_id (res_partner Many2one) field
    cr.execute("""UPDATE res_partner rp SET project_manager_id = CASE
        WHEN rp.project_manager = 'Alison' THEN 7
        WHEN rp.project_manager = 'Sylvain' THEN 3
        WHEN rp.project_manager = 'Julien' THEN 1344
        WHEN rp.project_manager = 'Coline' THEN 3926
    END
    WHERE rp.project_manager IS NOT NULL;
     """)

    # migrate project manager in res.partner
    env = api.Environment(cr, SUPERUSER_ID, {})
    child_partners = env['res.partner'].search([('parent_id', '!=', False)])
    for child in child_partners:
        parent = child.parent_id
        if False in (
        parent, parent.hebergement_omydoo, parent.type_eece_omydoo, parent.version_omydoo, parent.project_manager_id):
            continue
        if 'nop' in (parent.hebergement_omydoo, parent.type_eece_omydoo, parent.version_omydoo):
            continue
        child.write({
            'hebergement_omydoo': parent.hebergement_omydoo,
            'version_omydoo': parent.version_omydoo,
            'type_eece_omydoo': parent.type_eece_omydoo,
            'project_manager_id': parent.project_manager_id.id
        })



