function getToken() {
    return window.localStorage.getItem("token");
}

function setToken(jwtToken) {
    return window.localStorage.setItem("token", jwtToken);
}

function exchangeToken(accessToken) {
    return $.post({
        url: "/api/oauth/token",
        data: JSON.stringify({access_token: accessToken})
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