from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    utility_percentage = fields.Float(
        string='Porcentaje de Utilidad (%)', 
        default=15.0, 
        help='Porcentaje de la orden que se repartirá como utilidad entre los socios.'
    )
    
    utility_base_type = fields.Selection([
        ('subtotal', 'Subtotal (Sin Impuestos)'),
        ('total', 'Total (Con Impuestos)')
    ], string='Base de Cálculo', default='subtotal')

    total_utility = fields.Float(
        string='Utilidad Total', 
        compute='_compute_total_utility', 
        store=True
    )
    
    commission_record_ids = fields.One2many(
        'master.commission.record', 
        'sale_order_id', 
        string='Registros de Comisión',
        readonly=True
    )

    @api.model
    def default_get(self, fields_list):
        res = super(SaleOrder, self).default_get(fields_list)
        if 'utility_percentage' in fields_list and 'utility_percentage' not in res:
            res['utility_percentage'] = float(self.env['ir.config_parameter'].sudo().get_param('master_commission.default_percentage', 15.0))
        if 'utility_base_type' in fields_list and 'utility_base_type' not in res:
            res['utility_base_type'] = self.env['ir.config_parameter'].sudo().get_param('master_commission.default_base_type', 'subtotal')
        return res

    @api.depends('amount_untaxed', 'amount_total', 'utility_percentage', 'utility_base_type', 'order_line.product_id', 'order_line.price_subtotal', 'order_line.price_total')
    def _compute_total_utility(self):
        for order in self:
            total_util = 0.0
            for line in order.order_line:
                base_amount = line.price_subtotal if order.utility_base_type == 'subtotal' else line.price_total
                
                pct = order.utility_percentage
                if line.product_id and line.product_id.commission_percentage > 0:
                    pct = line.product_id.commission_percentage
                    
                total_util += ((base_amount or 0.0) * (pct or 0.0)) / 100.0
            order.total_utility = total_util

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        trigger = self.env['ir.config_parameter'].sudo().get_param('master_commission.generation_trigger', 'sale_confirm')
        if trigger == 'sale_confirm':
            self._generate_commissions()
        return res

    def _generate_commissions(self):
        for order in self:
            if order.total_utility > 0 and not order.commission_record_ids:
                partners = self.env['res.users'].search([('is_commission_partner', '=', True)])
                if partners:
                    total_weight = sum(partners.mapped('commission_weight'))
                    
                    for partner in partners:
                        if total_weight > 0:
                            partner_amount = order.total_utility * (partner.commission_weight / total_weight)
                        else:
                            partner_amount = order.total_utility / len(partners)
                            
                        if partner_amount > 0:
                            self.env['master.commission.record'].create({
                                'name': f'Comisión - {order.name}',
                                'sale_order_id': order.id,
                                'user_id': partner.id,
                                'amount': partner_amount,
                                'date': fields.Date.context_today(self),
                            })

    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        for order in self:
            # Si se cancela la orden, cancelamos las comisiones relacionadas
            if order.commission_record_ids:
                order.commission_record_ids.action_mark_cancel()
        return res
