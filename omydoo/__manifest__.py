# -*- coding: utf-8 -*-
{
    "name": "Omydoo",
    "summary": """
        Personnalisation d'Omydoo.""",
    "description": """
        V2.0.3 - 2025-01-21
        - [OMD-32]: ajout somme dans vue liste sur montant à facturer (AMS)
        - [OMD-132]: ajout de champs pour suivi étapes de tâches et popup pour demande de modifications (JSB)
        V2.0.2 - 2024-09-26
        - [OMD-90]: ajout fonctionnalité tâches liées et bloquée par dans les tâches (MAD)
        V2.0.1 - 2024-09-20
        - [OMD-85]: article bon de commande modifiable dans vue liste tâches et feuilles de temps (JSB)
        V15.9 - 2023-04-05
        - Ajout action planifiée pour passage tâche en done après 9 jours
        V15.8 - 2023-02-15
        - Ajout création tâche automatisé CII par le code
        V15.7 - 2023-01-31
        - Ajout de tags dans la vue form et kanban des contacts
        V15.6 - 2023-01-19
        - Ajout d'un champ GitHub dans les employés/warnings traités
        V15.5 - 2023-01-17
        - Ajout d'un numéro unique par tâche
        - Ajout des boutons copier/oeil pour sécuriser/améliorer les infos de l'instance dans les contacts
        V15.4 - 2022-08-23
        - Ajout du booléen backup True si hébergement nach_it sélectionné no modifié sinon
        V15.3 - 2022-08-08
        - Ajout du champ licence pour (visible si type enterprise est sélectionné)
        - Champ Lien de l'instance rendu cliquable
        V15.2 - 2022-02-25
        - Ajout background, ajout background logo, ajout du champs intégré par :
    """,
    "author": "Omydoo",
    "website": "https://www.omydoo.fr",
    "contributors": [
        "Sylvain Dubuisson <sylvain@omydoo.fr>",
        "Antoine Roffet <antoine@omydoo.fr>",
        "Antoine Deshayes <and@omydoo.fr>",
        "Justine Blanchet <jsb@omydoo.fr>",
        "Gabin Neron <gabinrn.pro@gmail.com>",
    ],
    "category": "Customizations",
    "version": "2.0.1",
    "application": True,
    # any module necessary for this one to work correctly ['module', 'another_one', ...]
    "depends": [
        "base",
        "helpdesk",
        "contacts",
        "hr",
        "project",
        "crm",
        "web_enterprise",
        "account_accountant",
        "base_automation",
        "l10n_fr",
        "sale_management",
        "hr_holidays",
        "l10n_fr_hr_holidays",
        "omd_expected_revenue",
        "omd_project_delivery",
        "hr_timesheet",
        "portal",
        "knowledge",
        "sale_subscription",
        "sale_project",
        "sale_timesheet",
    ],
    # always loaded
    "data": [
        "security/omydoo_security.xml",
        "security/ir.model.access.csv",
        "data/knowledge_article.xml",
        "data/ir_cron.xml",
        "data/ir_rules.xml",
        "data/mail_template.xml",
        "views/helpdesk_ticket.xml",
        "views/crm_lead.xml",
        "views/hr_employee.xml",
        "views/project.xml",
        "views/project_delivery.xml",
        "views/equipment_omydoo.xml",
        "views/account_move.xml",
        "views/res_partner.xml",
        "views/sale_order.xml",
        "views/push_tag.xml",
        "views/res_config_settings.xml",
        "views/odoo_hosting.xml",
        "views/odoo_version.xml",
        "views/omydoo_apps.xml",
        "views/timesheet.xml",
        "views/project_task_modification.xml",
        "reports/project_delivery_report.xml",
        "reports/sale_subscription_portal.xml",
        "data/options_modules.xml",
        "data/hosting_data.xml",
        "data/version_data.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "omydoo/static/src/css/form_button.css",
            "omydoo/static/src/css/tags_colors.css",
        ],
        "web.assets_frontend": [
            "omydoo/static/src/xml/signature_form.xml",
            "omydoo/static/src/js/signature_form.js",
            (
                "replace",
                "portal/static/src/signature_form/signature_form.js",
                "omydoo/static/src/js/signature_form.js",
            ),
        ],
        "web._assets_common_styles": [
            (
                "replace",
                "web_enterprise/static/src/legacy/scss/ui.scss",
                "omydoo/static/src/css/background_omydoo.scss",
            )
        ],
    },
    "license": "OPL-1",
}
