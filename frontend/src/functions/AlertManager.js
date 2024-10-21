import { ref } from 'vue';

const alerts = ref([]);

export function addAlert(type, content) {
    /**
     * Add Alert into alerts array.
     * this function return nothing.
     */
    alerts.value.push({type, content, isVisible: true});
    setTimeout(() => {
        alerts.value[alerts.value.length - 1].isVisible = false;
    }, 3000);
}

export function hideAlert(index) {
    /**
     * Hides alert at given index
     * this function return nothing.
     */
    alerts.value[index].isVisible = false;
}

export function useAlert() {
    /**
     * Get alert arrays.
     * @returns alerts array.
     */
    return { alerts };
}