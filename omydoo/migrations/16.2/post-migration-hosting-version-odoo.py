from odoo import api, fields, models, SUPERUSER_ID

def migrate(cr, version):
    # Créer une instance de l'environnement Odoo
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Dictonnaires de correspondance pour hebergement_omydoo
    hosting_mapping = {
        'odoo_sh': env.ref('omydoo.odoo_sh_hosting').id,
        'nach_it': env.ref('omydoo.cloudpepper_hosting').id,
        'onpremise': env.ref('omydoo.cloudpepper_hosting').id,
        'h8l': env.ref('omydoo.cloudpepper_hosting').id,
        'odoo_online': env.ref('omydoo.odoo_online_hosting').id
    }
    
    # Dictonnaires de correspondance pour version_omydoo
    version_mapping = {
        'v13': False,
        'v14': env.ref('omydoo.v14_version').id,
        'v15': env.ref('omydoo.v15_version').id,
        'v16': env.ref('omydoo.v16_version').id,
        'v17': env.ref('omydoo.v17_version').id
    }
    
    # Rechercher tous les enregistrements de res.partner
    partners = env['res.partner'].search([])

    for partner in partners:
        # Mettre à jour le champ odoo_hosting_id
        if partner.hebergement_omydoo in hosting_mapping:
            partner.odoo_hosting_id = hosting_mapping[partner.hebergement_omydoo]
        
        # Mettre à jour le champ odoo_version_id
        if partner.version_omydoo in version_mapping:
            partner.odoo_version_id = version_mapping[partner.version_omydoo]

