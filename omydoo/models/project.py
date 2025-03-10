from odoo import models, fields, api, SUPERUSER_ID
from datetime import date, timedelta, datetime
from odoo.exceptions import UserError


class ProjectDefault(models.Model):
    _inherit = "project.project"

    key = fields.Char(
        string="Clé", help="Clé du projet utilisée pour la génération des numéros de tâche"
    )
    task_sequence_id = fields.Many2one(
        "ir.sequence", string="Task Sequence", help="Sequence used for task numbers."
    )
    referent_dev_id = fields.Many2one("res.users", string="Développeur référent")
    etape_depart_client_omd = fields.Many2one(
        "project.task.type",
        string="Etape de départ pour les taches crées par les clients",
        domain="[('id','in',type_ids)]",
    )


class pprojectaskType(models.Model):
    _inherit = "project.task.type"

    default_steps = fields.Boolean("Étape par défaut", store=True, default=False)


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"


class ProjectTask(models.Model):
    _inherit = "project.task"

    linked_task_ids = fields.Many2many(
        "project.task",
        "project_task_link_rel",
        "task_id",
        "linked_task_id",
        domain="[('project_id', '=', project_id)]",
        string="Tâches liées",
    )

    blocked_by_task_ids = fields.Many2many(
        "project.task", compute="_compute_blocked_by_task_ids", string="Bloqué par", readonly=True
    )

    @api.depends("depend_on_ids")
    def _compute_blocked_by_task_ids(self):
        for task in self:
            task.blocked_by_task_ids = task.depend_on_ids

    task_number = fields.Char(string="Numéro de tâche", readonly=True)
    cii_field = fields.Html(string="Wiki")
    demandeur_ids = fields.Many2many(
        "res.users",
        relation="project_task_demandeur_rel",
        column1="task_id",
        column2="demandeur_id",
        string="Demandeurs",
        domain=lambda self: [("id", "in", self._get_internal_user_ids())],
        tracking=True,
        default=lambda self: [self.env.user.id],
    )
    user_ids = fields.Many2many(
        "res.users",
        relation="project_task_user_rel",
        column1="task_id",
        column2="user_id",
        string="Responsables",
        context={"active_test": False},
        tracking=True,
    )

    key_task = fields.Char(string="Clé-tâche", compute="_compute_concatenated_field", store=True)
    push_tag_ids = fields.Many2many(
        "push.tag",
        string="Étiquettes de push",
        help="Les étiquettes de push permettent d'indiquer si une action doit être menée au moment du push en production de la tâche",
    )
    referent_id = fields.Many2one(
        "res.users",
        string="Développeur référent",
        related="project_id.referent_dev_id",
        help="Le développeur référent n'est pas la personne responsable de la tâche mais le développeur référent du projet",
    )
    development_time = fields.Float("Temps de développement")
    testing_project_time = fields.Float("Temps de testing / Projet", compute="_compute_task_times")
    allocated_hours = fields.Float(
        "Temps alloué",
        compute="_compute_task_times",
        readonly=False,
        store=True,
        inverse="_inverse_compute_allocated_hours",
    )
    duplicable_development = fields.Boolean(
        "Développement duplicable",
        help="Un développement duplicable est une fonctionnalité générique pouvant être réutilisée sur n'importe quelle instance. La fonctionnalité sera développée dans un sous-module et ne doit donc pas dépendre d'autres champs spécifiques au client",
    )
    tutorial_link = fields.Char("Lien tuto Wiki")
    developer_description = fields.Html(
        "Description développeur",
        default=lambda self: (
            self.env.ref("omydoo.knowledge_article_dev_workflow", raise_if_not_found=False).body
            if self.env.ref("omydoo.knowledge_article_dev_workflow", raise_if_not_found=False)
            else ""
        ),
    )
    in_progress_date_stage = fields.Datetime(
        'Date de mise en étape "En cours"', compute="_compute_in_progress_date_stage", store=True
    )
    testing_dev_date_stage = fields.Datetime(
        'Date de mise en étape "Testing Dev"', compute="_compute_testing_dev_date_stage", store=True
    )
    testing_project_date_stage = fields.Datetime(
        'Date de mise en étape "Testing Projet"',
        compute="_compute_testing_project_date_stage",
        store=True,
    )
    modification_date_stage = fields.Datetime(
        'Date de mise en étape "Modification"',
        compute="_compute_modification_date_stage",
        store=True,
    )
    testing_customer_date_stage = fields.Datetime(
        'Date de mise en étape "Testing client"',
        compute="_compute_testing_customer_date_stage",
        store=True,
    )
    validation_date_stage = fields.Datetime(
        'Date de mise en étape "Validation"', compute="_compute_validation_date_stage", store=True
    )
    ready_to_push_date_stage = fields.Datetime(
        'Date de mise en étape "Ready to push"',
        compute="_compute_ready_to_push_date_stage",
        store=True,
    )
    on_prod_date_stage = fields.Datetime(
        'Date de mise en étape "On prod"', compute="_compute_on_prod_date_stage", store=True
    )
    modifications_ids = fields.One2many(
        "project.task.modification", "task_id", string="Modifcations"
    )

    @api.depends("stage_id")
    def _compute_in_progress_date_stage(self):
        for task in self:
            if task.stage_id.id == 124:
                task.in_progress_date_stage = datetime.now()

    @api.depends("stage_id")
    def _compute_testing_dev_date_stage(self):
        for task in self:
            if task.stage_id.id == 22:
                task.testing_dev_date_stage = datetime.now()

    @api.depends("stage_id")
    def _compute_testing_project_date_stage(self):
        for task in self:
            if task.stage_id.id == 458:
                task.testing_project_date_stage = datetime.now()

    @api.depends("stage_id")
    def _compute_modification_date_stage(self):
        for task in self:
            if task.stage_id.id == 678:
                task.modification_date_stage = datetime.now()

    @api.depends("stage_id")
    def _compute_testing_customer_date_stage(self):
        for task in self:
            if task.stage_id.id == 559:
                task.testing_customer_date_stage = datetime.now()

    @api.depends("stage_id")
    def _compute_validation_date_stage(self):
        for task in self:
            if task.stage_id.id == 144:
                task.validation_date_stage = datetime.now()

    @api.depends("stage_id")
    def _compute_ready_to_push_date_stage(self):
        for task in self:
            if task.stage_id.id == 665:
                task.ready_to_push_date_stage = datetime.now()

    @api.depends("stage_id")
    def _compute_on_prod_date_stage(self):
        for task in self:
            if task.stage_id.id == 334:
                task.on_prod_date_stage = datetime.now()

    def ask_for_task_modification(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Motif de modification",
            "res_model": "project.task.modification",
            "views": [[False, "form"]],
            "context": {"default_task_id": self.id, "default_user_id": self.env.user.id},
            "target": "new",
        }

    def onchange(self, values, field_names, fields_spec):
        context = self._context
        current_uid = context.get("uid")
        self.env.context = dict(self.env.context)
        user = self.env["res.users"].browse(current_uid)
        if user.share:
            project_id = context.get("default_project_id")
            stage_id = context.get("default_stage_id")
            current_project = self.env["project.project"].browse(project_id)
            permitted_stage_id = current_project.etape_depart_client_omd.id
            if not permitted_stage_id:
                raise UserError(
                    "L'étape de départ pour les taches crées par les clients n'est pas définie"
                )

            if stage_id != permitted_stage_id:
                raise UserError(
                    "Vous n'avez le droit de creer de tache que dans la colonne %s"
                    % current_project.etape_depart_client_omd.name
                )

        return super().onchange(values, field_names, fields_spec)

    @api.depends("development_time")
    def _compute_task_times(self):
        for task in self:
            testing_project_time = 0.00
            allocated_hours = 0.00
            if task.development_time:
                testing_project_time = (
                    task.development_time
                    * float(
                        self.env["ir.config_parameter"]
                        .sudo()
                        .get_param("omydoo.testing_project_coefficient")
                    )
                    or 0.4
                )
                allocated_hours = task.development_time + testing_project_time

            task.testing_project_time = testing_project_time
            task.allocated_hours = allocated_hours

    def _inverse_compute_allocated_hours(self):
        pass

    @api.onchange("stage_id")
    def _check_wiki_required(self):
        for task in self:
            if (
                task.stage_id.name == "Testing chef de projet"
                and not task.cii_field
                and any(tag.name in ["Dev", "Crisalid"] for tag in task.tag_ids)
            ):
                raise UserError("Le champ Wiki est requis pour les tâches de développement.")

    def _compute_display_name(self):
        for task in self:
            name = task.name
            if task.task_number and task.project_id:
                key = "[%s-%s]" % (task.project_id.key, task.task_number)
                name = "%s %s" % (key, name)
            task.display_name = name

    @api.model
    def _get_internal_user_ids(self):
        # Retourne une liste d'identifiants d'utilisateurs internes
        internal_users = self.env["res.users"].search([("share", "=", False)])
        return internal_users.ids

    @api.depends("task_number", "project_id.key")
    def _compute_concatenated_field(self):
        for task in self:
            if task.project_id and task.project_id.key and task.task_number:
                task.key_task = f"Tâche [{task.project_id.key}-{task.task_number}]"
            else:
                task.key_task = False

    def _create_tasks_for_project(self, project, task_number):
        task_sequence = self._get_or_create_project_sequence(project)

        # Vérifie si le projet a une clé
        if not project.key:
            raise UserError("Le champ 'Clé' du projet doit être spécifié.")

        # Vérifie si la tâche a déjà un numéro de tâche
        if not task_number:
            # Attribue un nouveau numéro de séquence uniquement aux nouvelles tâches
            next_task_number = task_sequence.next_by_code(f"project.task.sequence.{project.key}", 1)
            return next_task_number

    def _get_or_create_project_sequence(self, project):
        sequence_code = f"project.task.sequence.{project.key}"

        if not project.task_sequence_id:
            project.task_sequence_id = (
                self.env["ir.sequence"]
                .sudo()
                .create(
                    {
                        "name": f"Task Sequence - {project.name}",
                        "code": sequence_code,
                        "implementation": "standard",
                        "padding": 0,
                        "number_increment": 1,
                    }
                )
            )

        return project.task_sequence_id

    @api.model_create_multi
    def create(self, vals_list):
        context = self._context
        current_uid = context.get("uid")
        user = self.env["res.users"].browse(current_uid)
        for vals in vals_list:
            project_id = vals.get("project_id")
            if project_id:
                project = self.env["project.project"].browse(project_id)
                task_number = vals.get("task_number")
                next_task_number = self._create_tasks_for_project(project, task_number)
                vals["task_number"] = next_task_number
        if user.share:
            self.env.context = dict(self.env.context)
            self.env.context.update({"created_by_user": True})
        res_ids = super(ProjectTask, self).create(vals_list)
        return res_ids

    def copy(self, default=None):
        default = dict(default or {})
        project_id = self.project_id
        if project_id:
            task_number = self.task_number
            next_task_number = self._create_tasks_for_project(project_id, task_number)
            default["task_number"] = next_task_number

        return super().copy(default)

    @api.model
    def _action_cron_task_done(self):
        stage_done = self.env["project.task.type"].browse(123)
        tasks = self.search([("stage_id.name", "=", "On Prod")])
        for task in tasks:
            if task.date_last_stage_update.date() < (date.today() - timedelta(days=9)):
                task.write({"stage_id": stage_done.id})

    def _check_stage_change(self, vals):
        if "stage_id" in vals:
            for task in self:
                if task.stage_id.name == "Ready to push":
                    delivery_existed = (
                        self.env["project.delivery"]
                        .sudo()
                        .search(
                            [("project_id", "=", task.project_id.id), ("stage", "in", ["new"])],
                            limit=1,
                        )
                    )
                    line_values = {
                        "task_id": task.id,
                    }
                    if not task in delivery_existed.line_ids.mapped("task_id"):
                        if delivery_existed:
                            delivery_existed[0].sudo().write({"line_ids": [(0, 0, line_values)]})
                        else:
                            self.env["project.delivery"].sudo().with_user(SUPERUSER_ID).create(
                                {
                                    "name": "Développements",
                                    "project_id": task.project_id.id,
                                    "line_ids": [(0, 0, line_values)],
                                }
                            )

    def write(self, values):
        if (
            not self.env.context.get("request_for_modification")
            and "stage_id" in values
            and values.get("stage_id") == 678
        ):
            raise UserError("Merci d'effectuer une demande de modification")

        context = self._context
        current_uid = context.get("uid")
        user = self.env["res.users"].browse(current_uid)
        testing_client_preprod_string = "Testing client preprod"
        ready_to_push_string = "Ready to push"
        if user.share:
            values_bis = {}
            if values.get("stage_id"):
                values_bis["stage_id"] = values.get("stage_id")
            if values.get("sequence"):
                values_bis["sequence"] = values.get("sequence")
            if values.get("sequence") and not values.get("stage_id"):
                return 1

            if (
                values.get("description")
                and self.stage_id.id != self.project_id.etape_depart_client_omd.id
            ):
                raise UserError(
                    "Vous ne pouvez modifier le champs Description que dans la colonne %s"
                    % self.project_id.etape_depart_client_omd.name
                )
            elif (
                values.get("description")
                and self.stage_id.id == self.project_id.etape_depart_client_omd.id
            ):
                res = super(ProjectTask, self).write({"description": values.get("description")})
                self._check_stage_change(values)
                return res

            if context.get("created_by_user"):
                values["stage_id"] = self.project_id.etape_depart_client_omd.id
                res = super(ProjectTask, self).write(values)
                self._check_stage_change(values)
                return res
            if (
                values.get("stage_id")
                and self.stage_id
                and self.stage_id.name.lower().strip() == testing_client_preprod_string.lower()
                and self.env["project.task.type"]
                .browse(values.get("stage_id"))
                .name.lower()
                .strip()
                == ready_to_push_string.lower()
            ):
                res = super(ProjectTask, self).write(values_bis)
                self._check_stage_change(values)
                return res
            else:
                raise UserError(
                    'Vous ne pouvez modifier l\'état de cette tâche que de "Testing client preprod" à "Ready to push"'
                )

        else:
            res = super(ProjectTask, self).write(values)
            self._check_stage_change(values)
            return res
