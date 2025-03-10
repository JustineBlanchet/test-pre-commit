from odoo import models, exceptions

class KnowledgeArticle(models.Model):
    _inherit = 'knowledge.article'

    def _check_protected_knowledge_articles(self):
        articles = [self.env.ref('omydoo.knowledge_article_dev_workflow').id, self.env.ref('omydoo.knowledge_article_dev_space').id]
        for record in self:
            if record.id in articles:
                raise exceptions.UserError("Vous n'avez pas le droit de supprimer cet article de connaissance !")

    def unlink(self):
        self._check_protected_knowledge_articles()
        return super().unlink()

    def write(self, vals):
        if 'active' in vals and not vals.get('active'):
            self._check_protected_knowledge_articles()
        return super().write(vals)