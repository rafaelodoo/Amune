# ANTES (Causa del error)
# 'data': [
#     'security/ir.model.access.csv',
#     'views/stock_move_solicitud_wizard_views.xml', # <-- ESTA LÍNEA CAUSA EL ERROR
#     'views/stock_picking_views.xml',
# ],

# ==============================================================================
# DESPUÉS (Código corregido que debe estar en el archivo)
# ==============================================================================
# __manifest__.py
{
    'name': 'Calidad',
    'version': '1.0',
    'summary': 'Extensión del módulo de inventario para análisis de calidad.',
    'depends': [
        'stock',
        'quality_control',
        'quality'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizards/calidad_scrap_wizard_views.xml', # Añadir esta línea
        'views/stock_picking_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'calidad/static/src/css/style.css',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}