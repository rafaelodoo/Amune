from odoo import models, fields, api

class CalidadScrapWizard(models.TransientModel):
    _name = 'calidad.scrap.wizard'
    _description = 'Asistente para mover producto rechazado a desecho'

    move_id = fields.Many2one('stock.move', readonly=True)
    product_id = fields.Many2one(related='move_id.product_id', readonly=True)
    quantity = fields.Float(related='move_id.quantity', readonly=True, string="Cantidad Rechazada")

    # Este campo solo mostrará las ubicaciones de desecho.
    location_id = fields.Many2one(
        'stock.location',
        string='Ubicación de Desecho',
        domain="[('scrap_location', '=', True)]",
        required=True
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self.env.context.get('active_model') == 'stock.move' and self.env.context.get('active_id'):
            res['move_id'] = self.env.context['active_id']
        return res

    def action_scrap_product(self):
        # La lógica para mover el producto se añadirá aquí en el futuro.
        # Por ahora, simplemente cerramos el wizard.
        self.ensure_one()
        return {'type': 'ir.actions.act_window_close'}