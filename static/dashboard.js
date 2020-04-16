function getToken() {
    return window.localStorage.getItem("token");
}

function setToken(jwtToken) {
    return window.localStorage.setItem("token", jwtToken);
}

function exchangeToken(code) {
    return $.post({
        url: "/api/oauth/token",
        data: JSON.stringify({code: code})
    });
}

function apiRequest(method, url, data) {
    const token = getToken();
    if (token === null) {
        throw "You need to login";
    }

    return $.ajax({
        method: method,
        url: url,
        data: data,
        headers: {Authorization: token}
    });
}

$(() => {
    if (getToken() !== null) return;
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");

    if (code === null) {
        window.location.href = "/dashboard/login";
    }

    exchangeToken(code).done(resp => {
        setToken(resp.token);
    }).fail((resp) => {
        window.location.href = "/dashboard/login";
    })
});