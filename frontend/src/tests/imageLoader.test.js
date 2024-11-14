import { loadImage } from '@/functions/Utils';

describe('loadImage', () => {
    let fileReaderMock;
    beforeEach(() => {
        fileReaderMock = {
            readAsDataURL: jest.fn(),
            onload: null,
            onerror: null,
            result: 'data:image/jpeg;base64,...',
        };
        global.FileReader = jest.fn(() => fileReaderMock);
    });

    it('Success with Data URL when image is successfully loaded', async () => {
        const mockFile = new Blob(['image content'], { type: 'image/jpeg' });
        const promise = loadImage(mockFile);
        fileReaderMock.onload({ target: fileReaderMock });
        await expect(promise).resolves.toBe('data:image/jpeg;base64,...');
    });

    it('Reject with an error if the file cannot be loaded', async () => {
        const mockFile = new Blob(['image content'], { type: 'image/jpeg' });
        const promise = loadImage(mockFile);
        fileReaderMock.onerror(new Error('File reading error'));
        await expect(promise).rejects.toThrow('File reading error');
    });

    it('Call readAsDataURL with the correct file', () => {
        const mockFile = new Blob(['image content'], { type: 'image/jpeg' });
        loadImage(mockFile);
        expect(fileReaderMock.readAsDataURL).toHaveBeenCalledWith(mockFile);
    });
});
