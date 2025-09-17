/** @odoo-module **/

import { ListRenderer } from "@web/views/list/list_renderer";
import { patch } from "@web/core/utils/patch";
import { onPatched } from "@odoo/owl";

patch(ListRenderer.prototype, {
    setup() {
        super.setup();
        onPatched(() => {
            this._updateQualityButtons();
        });
    },

    _updateQualityButtons() {
        if (!this.tbody) {
            return;
        }
        this.tbody.querySelectorAll(":scope > tr.o_data_row").forEach(tr => {
            const recordId = tr.dataset.id;
            const record = this.props.list.records.find(rec => rec.id === recordId);
            if (!record || !record.data.quality_status) {
                return;
            }
            const qualityStatus = record.data.quality_status;
            tr.querySelectorAll(".o_quality_button").forEach(btn => {
                btn.style.display = 'none';
            });
            tr.querySelectorAll(`.o_quality_${qualityStatus}`).forEach(btn => {
                btn.style.display = 'inline-block';
            });
        });
    }
});