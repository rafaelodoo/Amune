/** @odoo-module **/

import { registry } from "@web/core/registry";
import { formView } from "@web/views/form/form_view";
import { useEffect } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class StockPickingFormController extends formView.Controller {
    setup() {
        super.setup();
        
        this.notification = useService("notification");
        
        // Usar useEffect para manejar la actualización del botón
        useEffect(
            () => this.updateButtons(),
            () => [this.model.root.data.has_zero_quantities]
        );
        
        // Usar useEffect para manejar la visibilidad de la columna verificacion_visual
        useEffect(
            () => this.updateVerificacionVisual(),
            () => [this.model.root.data.show_verificacion_visual]
        );
    }

    /**
     * Actualiza el estado del botón "Confirmar pesos" basado en el valor de has_zero_quantities
     */
    updateButtons() {
        try {
            const confirmButton = document.querySelector('button[name="action_confirm_weights"]');
            if (!confirmButton) {
                console.log('Botón de confirmar pesos no encontrado');
                return;
            }

            const hasZeroQuantities = this.model.root.data.has_zero_quantities;
            
            if (hasZeroQuantities) {
                confirmButton.setAttribute('disabled', 'disabled');
                confirmButton.classList.remove('oe_highlight');
                confirmButton.classList.add('disabled');
            } else {
                confirmButton.removeAttribute('disabled');
                confirmButton.classList.add('oe_highlight');
                confirmButton.classList.remove('disabled');
            }
        } catch (error) {
            console.error('Error al actualizar el estado del botón:', error);
        }
    }
    
    /**
     * Actualiza la visibilidad de la columna de verificación visual
     */
    updateVerificacionVisual() {
        try {
            const showVerificacionVisual = this.model.root.data.show_verificacion_visual;
            const table = document.querySelector('.o_list_table');
            
            if (!table) {
                console.log('Tabla de movimientos no encontrada');
                return;
            }
            
            // Encuentra el índice de la columna verificacion_visual
            const headers = table.querySelectorAll('thead th');
            let verificacionIndex = -1;
            
            // Buscar el índice basado en el atributo data-name
            for (let i = 0; i < headers.length; i++) {
                if (headers[i].getAttribute('data-name') === 'verificacion_visual') {
                    verificacionIndex = i;
                    break;
                }
            }
            
            if (verificacionIndex === -1) {
                // Si no encontramos por data-name, busquemos por el texto del encabezado
                for (let i = 0; i < headers.length; i++) {
                    if (headers[i].textContent.trim() === 'Verif. Visual') {
                        verificacionIndex = i;
                        break;
                    }
                }
            }
            
            if (verificacionIndex !== -1) {
                // Ajustar para que sea 0-indexado para el querySelector
                const colIndex = verificacionIndex;
                
                // Actualizar visibilidad del encabezado
                headers[colIndex].style.display = showVerificacionVisual ? '' : 'none';
                
                // Actualizar visibilidad de las celdas
                const rows = table.querySelectorAll('tbody tr');
                for (const row of rows) {
                    const cells = row.querySelectorAll('td');
                    if (cells.length > colIndex) {
                        cells[colIndex].style.display = showVerificacionVisual ? '' : 'none';
                    }
                }
            }
        } catch (error) {
            console.error('Error al actualizar la visibilidad de la columna:', error);
        }
    }
    
    /**
     * Sobreescribir el método onButtonClicked para actualizar la vista después de confirmar pesos
     * @override
     */
    async onButtonClicked(ev) {
        const result = await super.onButtonClicked(ev);
        
        // Verificar si la acción es confirmar pesos
        if (ev.name === 'action_confirm_weights') {
            // Forzar una renderización de la vista después de confirmar pesos
            await this.model.root.load();
            this.updateVerificacionVisual();
            
            // Mostrar notificación de éxito
            if (result && result.context && result.context.notification_message) {
                this.notification.add(
                    result.context.notification_message,
                    { type: result.context.notification_type || 'success' }
                );
            }
        }
        
        return result;
    }
}

// Registrar la vista personalizada
registry.category("views").add("stock_picking_form_view_button", {
    ...formView,
    Controller: StockPickingFormController,
}); 