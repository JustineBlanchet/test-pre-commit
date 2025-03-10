from odoo import models, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    medium_id = fields.Many2one()

    chef_projet = fields.Char(string="Chef de projet chez le partenaire")
    nom_entreprise_client = fields.Char(string="Nom de l'entreprise du client")
    adresse_entreprise_client = fields.Text(string="Adresse de l'entreprise (complète)")
    tva = fields.Char(string="TVA")
    secteur_activite = fields.Char(string="Secteur d'activité")
    nom_prenom_client = fields.Char(string="Nom et prénom du client")
    position_client = fields.Char(string="Position du client")
    telephone_client = fields.Char(string="Numéro de téléphone du client")
    email_client = fields.Char(string="Adresse mail du ou des clients (pour l'envoi du devis)")
    type_abonnement = fields.Selection([('custom', 'CUSTOM'), ('standard', 'STANDARD')])
    hebergement = fields.Selection([('odoosh', 'ODOO SH'), ('saas', 'SAAS'), ('onpremise', 'ON PREMISE')], string="Hébergement")
    workers = fields.Integer(string="Nombre de workers")
    staging = fields.Integer(string="Nombre de staging")
    gb = fields.Integer(string="Nombre de Gb")
    nombre_utilisateurs = fields.Char(string="Nombre d'utilisateurs")
    nombre_utilisateurs_terme = fields.Char(string="Nombre d'utilisateurs à terme")
    nombre_employes = fields.Char(string="Nombre d'employés", default=False)
    modules_interesses = fields.Many2many('module.options', string='Modules intéressés')
    departement_travail_odoo = fields.Text(string="Département travaillant avec Odoo")
    departement_non_travail_odoo = fields.Char(string="Département ne travaillant pas avec Odoo")
    description_flux_entreprise = fields.Text(string="Description complète des flux de l'entreprise")
    informations_negociation = fields.Text(string="Informations importantes pour la négociation du contrat")
    systeme_actuel = fields.Char(string="Système actuel (que Odoo va remplacer)")
    raison_recherche_nouvel_erp = fields.Text(string="Pourquoi cherchent-ils un nouvel ERP ?")
    problemes_actuels = fields.Text(string="Problèmes actuels rencontrés")
    logiciels_interfacer_odoo = fields.Text(string="Logiciels devant être interfacés avec Odoo")
    developpements_specifiques = fields.Text(string="Développements spécifiques prévus")
    risque_potentiel_projet = fields.Text(string="Risques potentiels pour le projet")
    date_lancement_projet = fields.Date(string="Date de mise en lancement du projet et signature")
    budget_implementation = fields.Char(string="Budget pour l'implémentation")
    contrat_multi_annee = fields.Char(string="Contrat Odoo multi-année, si oui, combien?")
    petite_description = fields.Text(string="Petite description")
    longue_description = fields.Text(string="Longue description")
