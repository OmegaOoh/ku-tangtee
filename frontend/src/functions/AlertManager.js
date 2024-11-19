import { ref } from 'vue';

const alerts = ref([]);

export function addAlert(type, content) {
    /**
     * Add Alert into alerts array.
     * this function return nothing.
     */
    alerts.value.push({ type, content, isVisible: false }); // Create obj
    const index = alerts.value.length - 1;
    alerts.value[index].isVisible = true;
    setTimeout(() => {
        hideAlert(index);
    }, 3000);
}

export function hideAlert(index) {
    /**
     * Hides alert at given index
     * this function return nothing.
     */
    if (alerts.value[index]) {
        alerts.value[index].isVisible = false;
    }
}

export function useAlert() {
    /**
     * Get alert arrays.
     * @returns alerts array.
     */
    return { alerts };
}
