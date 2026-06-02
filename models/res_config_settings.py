from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    commission_default_percentage = fields.Float(
        string='Porcentaje de Utilidad Predeterminado',
        config_parameter='master_commission.default_percentage',
        default=15.0,
        help='El porcentaje que se usará por defecto en las nuevas órdenes de venta.'
    )
    
    commission_default_base_type = fields.Selection([
        ('subtotal', 'Subtotal (Sin Impuestos)'),
        ('total', 'Total (Con Impuestos)')
    ], string='Base de Cálculo Predeterminada',
       config_parameter='master_commission.default_base_type',
       default='subtotal',
       help='Si la comisión se calcula sobre el subtotal o el total con impuestos.')

    commission_generation_trigger = fields.Selection([
        ('sale_confirm', 'Confirmación de Venta'),
        ('invoice_validate', 'Validación de Factura')
    ], string='Detonante de Comisiones',
       config_parameter='master_commission.generation_trigger',
       default='sale_confirm',
       required=True,
       help='Cuándo se debe generar el registro de comisión de forma automática.')
