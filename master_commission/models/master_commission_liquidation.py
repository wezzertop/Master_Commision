from odoo import models, fields, api

class MasterCommissionLiquidation(models.Model):
    _name = 'master.commission.liquidation'
    _description = 'Liquidación Masiva de Comisiones'
    _order = 'date desc, id desc'

    name = fields.Char(string='Referencia', required=True, copy=False, default='Nueva Liquidación')
    user_id = fields.Many2one('res.users', string='Socio', required=True)
    date = fields.Date(string='Fecha', required=True, default=fields.Date.context_today)
    
    commission_ids = fields.One2many(
        'master.commission.record', 
        'liquidation_id', 
        string='Comisiones Incluidas'
    )
    
    total_amount = fields.Float(
        string='Total a Pagar', 
        compute='_compute_total_amount', 
        store=True
    )

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('done', 'Liquidada (Pagada)'),
        ('cancel', 'Cancelada')
    ], string='Estado', default='draft', required=True, tracking=True)

    @api.depends('commission_ids.amount')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.commission_ids.mapped('amount'))

    def action_mark_done(self):
        for record in self:
            if record.state == 'draft':
                record.state = 'done'
                # Marcar todas las comisiones hijas como pagadas
                record.commission_ids.write({'state': 'paid'})

    def action_mark_cancel(self):
        for record in self:
            record.state = 'cancel'
            # Devolver las comisiones a borrador
            record.commission_ids.write({'state': 'draft', 'liquidation_id': False})

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nueva Liquidación') == 'Nueva Liquidación':
            # Asignar un nombre único basado en fecha
            vals['name'] = f'LIQ-{fields.Date.context_today(self)}'
        return super(MasterCommissionLiquidation, self).create(vals)
