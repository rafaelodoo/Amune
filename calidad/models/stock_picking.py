# models/stock_picking.py
from odoo import models, fields, api
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = 'stock.move'

    # --- CAMPOS EXISTENTES ---
    quality_check_id = fields.Many2one(
        'quality.check',
        string='Control de Calidad',
        copy=False,
        readonly=True
    )
    quality_check_state = fields.Selection(
        related='quality_check_id.quality_state',
        string="Estado de Calidad"
    )
    quality_point_id = fields.Many2one(
        'quality.point',
        string="Punto de Control de Calidad",
        compute='_compute_quality_point_id',
        store=True
    )

    # --- MÉTODOS EXISTENTES ---
    @api.depends('product_id', 'picking_id.picking_type_id')
    def _compute_quality_point_id(self):
        for move in self:
            move.quality_point_id = self.env['quality.point'].search([
                ('picking_type_ids', 'in', move.picking_id.picking_type_id.id),
                '|',
                ('product_ids', 'in', move.product_id.id),
                ('product_category_ids', 'in', move.product_id.categ_id.ids)
            ], limit=1)

    def action_solicitud_analisis(self):
        for move in self:
            if not move.quality_point_id:
                raise UserError("No existe un punto de control de calidad configurado para este producto en esta operación.")
            if move.quality_check_id:
                raise UserError("Ya se ha generado un control de calidad para esta línea.")
            quality_check = self.env['quality.check'].create({
                'picking_id': move.picking_id.id,
                'product_id': move.product_id.id,
                'company_id': move.company_id.id,
                'point_id': move.quality_point_id.id,
                'team_id': move.quality_point_id.team_id.id,
            })
            move.quality_check_id = quality_check.id
        return True

    def action_view_quality_check(self):
        self.ensure_one()
        if not self.quality_check_id:
            raise UserError("No se encontró un control de calidad asociado a esta línea.")
        return {
            'name': 'Control de Calidad',
            'type': 'ir.actions.act_window',
            'res_model': 'quality.check',
            'view_mode': 'form',
            'res_id': self.quality_check_id.id,
            'target': 'current',
        }

    # =============================================================
    # MÉTODOS DE REPORTE CORREGIDOS
    # =============================================================
    def action_print_report_ram(self):
        """
        Llama al reporte 'Externa' (quality_worksheet).
        """
        self.ensure_one()
        if not self.quality_check_id:
            raise UserError("No existe un control de calidad para generar este reporte.")
        
        # Forma correcta y robusta de llamar a un reporte por su nombre.
        report = self.env['ir.actions.report']._get_report_from_name('quality_control.quality_worksheet')
        return report.report_action(self.quality_check_id)

    def action_print_report_cer(self):
        """
        Llama al reporte 'Interna' (quality_worksheet_internal).
        """
        self.ensure_one()
        if not self.quality_check_id:
            raise UserError("No existe un control de calidad para generar este reporte.")

        # Forma correcta y robusta de llamar a un reporte por su nombre.
        report = self.env['ir.actions.report']._get_report_from_name('quality_control.quality_worksheet_internal')
        return report.report_action(self.quality_check_id)
        
    def action_open_scrap_wizard(self):
        self.ensure_one()
        return {
            'name': 'Enviar a Desecho',
            'type': 'ir.actions.act_window',
            'res_model': 'calidad.scrap.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_move_id': self.id,
            }
        }