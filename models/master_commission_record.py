from odoo import models, fields, api

class MasterCommissionRecord(models.Model):
    _name = 'master.commission.record'
    _description = 'Registro de Comisión de Socio'
    _order = 'date desc, id desc'

    name = fields.Char(string='Referencia', required=True, copy=False)
    sale_order_id = fields.Many2one('sale.order', string='Orden de Venta', ondelete='cascade', required=True)
    partner_id = fields.Many2one('res.partner', related='sale_order_id.partner_id', string='Cliente', store=True, readonly=True)
    user_id = fields.Many2one('res.users', string='Socio', ondelete='cascade', required=True)
    amount = fields.Float(string='Monto de Comisión', required=True)
    date = fields.Date(string='Fecha', required=True, default=fields.Date.context_today)
    
    liquidation_id = fields.Many2one(
        'master.commission.liquidation', 
        string='Liquidación', 
        ondelete='set null'
    )
    
    sale_total_utility = fields.Float(
        related='sale_order_id.total_utility', 
        string='Utilidad Total de Venta', 
        store=True, 
        readonly=True
    )
    
    product_ids = fields.Many2many(
        'product.product', 
        compute='_compute_product_ids', 
        string='Productos Vendidos',
        store=True
    )
    
    @api.depends('sale_order_id.order_line.product_id')
    def _compute_product_ids(self):
        for record in self:
            record.product_ids = record.sale_order_id.order_line.mapped('product_id')
    
    state = fields.Selection([
        ('draft', 'Pendiente'),
        ('paid', 'Pagada'),
        ('cancel', 'Cancelada')
    ], string='Estado', default='draft', required=True, tracking=True)

    def action_mark_paid(self):
        for record in self:
            if record.state == 'draft':
                record.state = 'paid'

    def action_mark_cancel(self):
        for record in self:
            record.state = 'cancel'
