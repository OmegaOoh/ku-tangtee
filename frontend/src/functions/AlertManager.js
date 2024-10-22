import { ref } from 'vue';

const alerts = ref([]);

export function addAlert(type, content) {
    /**
     * Add Alert into alerts array.
     * this function return nothing.
     */
    alerts.value.push({type, content, isVisible: true});
    setTimeout(() => {
        hideAlert(0);
    }, 3000);
}

export function hideAlert(index) {
    /**
     * Hides alert at given index
     * this function return nothing.
     */
    alerts.value[index].isVisible = false;
    alerts.value.splice(index, 1);
}

export function useAlert() {
    /**
     * Get alert arrays.
     * @returns alerts array.
     */
    return { alerts };
}