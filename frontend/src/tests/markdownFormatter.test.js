import { markdownFormatter } from '@/functions/Utils';
import DOMPurify from 'dompurify';

// Mocking the sanitize method of DOMPurify for testing
jest.mock('dompurify', () => ({
    sanitize: jest.fn((input) => input),
}));

describe('markdownFormatter', () => {
    it('Return empty string when it is null or nothing', () => {
        expect(markdownFormatter(null)).toBe('');
        expect(markdownFormatter('')).toBe('');
        expect(markdownFormatter('   ')).toBe('');
    });

    it('Return format link correctly', () => {
        const input = '[OpenAI](https://linktr.ee/)';
        const output = markdownFormatter(input);
        expect(output).toContain(
            '<a href="https://linktr.ee/" target="_blank" class="text-accent hover:brightness-75 underline">OpenAI</a>'
        );
    });

    it('Return format list correctly', () => {
        const input = '- Item 1\n- Item 2\n1. Ordered item\n2. Ordered item 2';
        const output = markdownFormatter(input);
        expect(output).toContain('<li class="ml-3 list-disc"> Item 1</li>');
        expect(output).toContain(
            '<li class="ml-3 list-decimal"> Ordered item</li>'
        );
    });

    it('Return format codeblock correctly', () => {
        const input = '```javascript\nconst x = 10;\n```';
        const output = markdownFormatter(input);
        expect(output).toContain(
            "<div class='relative m-2 rounded-lg overflow-hidden'>"
        );

        expect(output).toMatch(/<pre.*class=".*hljs.*language-javascript.*">/);
    });

    it('Return format inline code correctly', () => {
        const input = 'This is `inline code`';
        const output = markdownFormatter(input);
        expect(output).toContain(
            "<code class='bg-neutral-focus bg-opacity-75 px-1 rounded-sm overflow-hidden'>inline code</code>"
        );
    });

    it('Display raw image markdown correctly', () => {
        const input = '![Image](https://example.com/image.jpg)';
        const output = markdownFormatter(input);
        expect(output).toContain(
            '<span>![Image](https://example.com/image.jpg)</span>'
        );
    });

    it('Clean output', () => {
        const input = '<script>alert("XSS")</script>';
        markdownFormatter(input);
        expect(DOMPurify.sanitize).toHaveBeenCalled();
    });
});
