from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        # Primero ejecutar la lógica original de Odoo para publicar la factura
        res = super(AccountMove, self).action_post()
        
        # Revisar si el detonante de comisiones está configurado en "Validación de Factura"
        trigger = self.env['ir.config_parameter'].sudo().get_param('master_commission.generation_trigger', 'sale_confirm')
        
        if trigger == 'invoice_validate':
            for move in self:
                # Solo nos interesan las facturas de clientes (no de proveedores ni otros tipos)
                if move.move_type == 'out_invoice':
                    # Buscar las Órdenes de Venta relacionadas a esta factura
                    # En Odoo 16/17/18, las líneas de factura están ligadas a las líneas de venta
                    sale_orders = move.invoice_line_ids.mapped('sale_line_ids.order_id')
                    
                    if sale_orders:
                        # Generar comisiones para las órdenes de venta relacionadas (si no se han generado aún)
                        sale_orders._generate_commissions()

                elif move.move_type == 'out_refund':
                    # Es una Nota de Crédito / Devolución
                    sale_orders = move.invoice_line_ids.mapped('sale_line_ids.order_id')
                    for order in sale_orders:
                        # Buscamos si ya se habían pagado comisiones por esta venta
                        existing_commissions = self.env['master.commission.record'].search([
                            ('sale_order_id', '=', order.id),
                            ('amount', '>', 0)
                        ])
                        if existing_commissions:
                            # Generar comisiones negativas para descontar el dinero a los socios
                            # Proporcional al monto de la nota de crédito vs el total de la venta
                            refund_ratio = move.amount_total / order.amount_total if order.amount_total else 1.0
                            
                            for comm in existing_commissions:
                                self.env['master.commission.record'].create({
                                    'name': f'Devolución - {move.name} ({order.name})',
                                    'sale_order_id': order.id,
                                    'user_id': comm.user_id.id,
                                    'amount': -(comm.amount * refund_ratio),
                                    'date': fields.Date.context_today(self),
                                    'state': 'draft' # Entra como borrador para la próxima liquidación
                                })
                        
        return res
