import { addAlert, useAlert, hideAlert } from '@/functions/AlertManager';
import { nextTick } from 'vue';

jest.useFakeTimers();

describe('Alert functions', () => {
    beforeEach(() => {
        useAlert().alerts.value = [];
    });

    it('Adds an alert with type, content, and isVisible set to true', () => {
        addAlert('success', 'This is a success message');
        const { alerts } = useAlert();
        expect(alerts.value.length).toBe(1);
        expect(alerts.value[0]).toEqual({
            type: 'success',
            content: 'This is a success message',
            isVisible: true,
        });
    });

    it('Automatically hides an alert after 3 seconds', async () => {
        addAlert('error', 'This is an error message');
        const { alerts } = useAlert();
        expect(alerts.value.length).toBe(1);
        jest.runAllTimers();
        await nextTick();
        expect(alerts.value.length).toBe(0);
    });

    it('hides and removes an alert when hideAlert is called', () => {
        addAlert('info', 'This is an info message');
        const { alerts } = useAlert();
        expect(alerts.value.length).toBe(1);
        hideAlert(0);
        expect(alerts.value.length).toBe(0);
    });

    it('useAlert returns the alerts array', () => {
        const { alerts } = useAlert();
        expect(Array.isArray(alerts.value)).toBe(true);
        expect(alerts.value).toEqual([]);
    });
});
