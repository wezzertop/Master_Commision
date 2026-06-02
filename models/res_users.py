from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    is_commission_partner = fields.Boolean(
        string='Es Socio de Comisiones',
        default=False,
        help='Si está marcado, este usuario recibirá una parte de la utilidad de las ventas.'
    )

    commission_weight = fields.Float(
        string='Peso de Comisión (%)',
        default=100.0,
        help='Proporción matemática para calcular cuánto le toca a este socio de la bolsa de comisiones.'
    )
