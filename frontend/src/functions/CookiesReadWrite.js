export function setCookie(id, value, minuteLifetime) {
    var now = new Date();
    const time = now.getTime();
    var expireTime = time + minuteLifetime * 60 * 1000;
    now.setTime(expireTime);
    const exp = now.toUTCString();
    document.cookie = `${id}=${value};expires=${exp};`;
}

export function deleteCookie(id) {
    document.cookie = id + '=;';
}

export function getCookie(id) {
    let value = document.cookie.match('(^|;)?' + id + '=([^;]*)(;|$)');
    return value ? value[2] : null;
}
