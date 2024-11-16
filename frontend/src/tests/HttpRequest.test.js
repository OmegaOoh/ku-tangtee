import apiClient from '@/api';
import {
    getCsrfToken,
    createPostRequest,
    createPutRequest,
    createDeleteRequest,
} from '@/functions/HttpRequest';

jest.mock('@/api');

describe('API Request Functions', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    describe('getCsrfToken', () => {
        it('Fetch CSRF token from the server', async () => {
            const mockToken = 'testCsrfToken';
            apiClient.get.mockResolvedValue({ data: { csrfToken: mockToken } });

            const csrfToken = await getCsrfToken();
            expect(apiClient.get).toHaveBeenCalledWith(
                '/activities/get-csrf-token/'
            );
            expect(csrfToken).toBe(mockToken);
        });
    });

    describe('createPostRequest', () => {
        it('Make a POST request with CSRF token in headers', async () => {
            const mockPath = '/test/post';
            const mockData = { key: 'value' };
            const mockToken = 'testCsrfToken';
            apiClient.get.mockResolvedValue({ data: { csrfToken: mockToken } });
            apiClient.post.mockResolvedValue({ status: 200, data: {} });
            const response = await createPostRequest(mockPath, mockData);
            expect(apiClient.get).toHaveBeenCalledWith(
                '/activities/get-csrf-token/'
            );
            expect(apiClient.post).toHaveBeenCalledWith(mockPath, mockData, {
                headers: { 'X-CSRFToken': mockToken },
            });
            expect(response.status).toBe(200);
        });
    });

    describe('createPutRequest', () => {
        it('Make a PUT request with CSRF token in headers', async () => {
            const mockPath = '/test/put';
            const mockData = { key: 'value' };
            const mockToken = 'testCsrfToken';
            apiClient.get.mockResolvedValue({ data: { csrfToken: mockToken } });
            apiClient.put.mockResolvedValue({ status: 200, data: {} });
            const response = await createPutRequest(mockPath, mockData);
            expect(apiClient.get).toHaveBeenCalledWith(
                '/activities/get-csrf-token/'
            );
            expect(apiClient.put).toHaveBeenCalledWith(mockPath, mockData, {
                headers: { 'X-CSRFToken': mockToken },
            });
            expect(response.status).toBe(200);
        });
    });

    describe('createDeleteRequest', () => {
        it('Make a DELETE request with CSRF token in headers', async () => {
            const mockPath = '/test/delete';
            const mockToken = 'testCsrfToken';
            apiClient.get.mockResolvedValue({ data: { csrfToken: mockToken } });
            apiClient.delete.mockResolvedValue({ status: 200, data: {} });
            const response = await createDeleteRequest(mockPath);
            expect(apiClient.get).toHaveBeenCalledWith(
                '/activities/get-csrf-token/'
            );
            expect(apiClient.delete).toHaveBeenCalledWith(mockPath, {
                headers: { 'X-CSRFToken': mockToken },
            });
            expect(response.status).toBe(200);
        });
    });
});
