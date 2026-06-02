from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    commission_percentage = fields.Float(
        string='Porcentaje de Comisión (%)',
        default=0.0,
        help='Si es mayor a 0, este porcentaje se usará para calcular la comisión de este producto, ignorando el porcentaje global de la orden de venta.'
    )
