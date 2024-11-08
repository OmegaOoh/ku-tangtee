import {marked} from "marked";
import DOMPurify from "dompurify";

export function loadImage(imgFile) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        
        reader.onload = (e) => {
        resolve(e.target.result); // Resolve with the Data URL
        };
        
        reader.onerror = (error) => {
        reject(error); // Reject on error
        };
        reader.readAsDataURL(imgFile); // Read the file as a Data URL
    })
}

export function markdownFormatter(string) {
    /*
     * Format message to be html format, with some md properties
     *
     * @params {string} not yet formatted message
     * @returns {string} formatted message
     */
    if (!string || string.trim() == '') return ''
    const renderer = new marked.Renderer();

    // Set style to link
    renderer.link = (token) => {
        return `<a href="${token.href}" target="_blank" class="text-accent hover:brightness-75 underline">${token.text || token.raw}</a>`;
    };
    // Prevent using html to add image
    renderer.image = (token) => {
        return `<span>${token.raw}</span>`
    }
    
    renderer.listitem = (token) => {
        let type = 'list-decimal'
        if (token.raw[0] == '-' || token.raw[0] == '*') type = 'list-disc'
        return `<li class="ml-3 ${type}"> ${token.text}</li>`
    }

    renderer.code = (token) => {
        return `<pre v-highlightjs><code class="${token.lang}">${token.text}</code></pre>`
    }

    let parsed_msg = marked(string, { renderer });
    
    parsed_msg = parsed_msg.replace(/\n/g, '<br>')
                    .replace(/(<ul>|<ol>)(\s*<br\s*\/?>\s*)+/g, '$1') // Remove leading <br> after <ul> or <ol>
                    .replace(/(\s*<br\s*\/?>)+\s*(<\/li>)/g, '$2') // Remove <br> before </li>
                    .replace(/^\s*<br\s*\/?>/gm, '') // remove leading <br>
                    .replace(/<br>$/, '') // remove trailing blank lines
    
    return DOMPurify.sanitize(parsed_msg);
}
