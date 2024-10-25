export function setCookie(id, value) {

    document.cookie = id + '=' + value;
}

export function deleteCookie(id) {

    document.cookie = id + '=;';
}

export function getCookie(id) {

    let value = document.cookie.match('(^|;)?' + id + '=([^;]*)(;|$)');
    return value ? value[2] : null;
}