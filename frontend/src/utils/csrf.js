export function getCsrfToken() {
    /*
     * Trying to get CSRF Token.
     * @returns {string} CSRF Token.
     */
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith("csrftoken=")) {
                cookieValue = decodeURIComponent(
                    cookie.substring("csrftoken=".length)
                );
                break;
            }
        }
    }
    return cookieValue;
}
