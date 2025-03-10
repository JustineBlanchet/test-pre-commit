from odoo import fields, models, api


class ProductProductInherited(models.Model):
    _inherit = 'product.product'

    def get_product_multiline_description_sale(self):
        original_name = super(ProductProductInherited, self).get_product_multiline_description_sale()
        # prevent error if we add note to quotation template
        if not original_name:
            return
        return original_name.replace(self.display_name + '\n', '')
