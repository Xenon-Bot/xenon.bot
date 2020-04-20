function getToken() {
    return window.localStorage.getItem("token");
}

function setToken(jwtToken) {
    return window.localStorage.setItem("token", jwtToken);
}

function deleteToken() {
    window.localStorage.removeItem("token");
}

function logout() {
    deleteToken();
    window.location.reload();
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
        headers: {Authorization: token},
        statusCode: {
            401: () => {
                logout();
            }
        }
    });
}

$(() => {
    function dispatchLogin() {
        apiRequest("GET", "/api/oauth/user").done(resp => {
            const event = new CustomEvent("login", {detail: {user: resp}});
            window.dispatchEvent(event);
        })
    }

    $(window).on("login", e => {
        const user = e.detail.user;
        $(".load-user-name").html(user.username);
    });

    if (getToken() == null) {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get("code");

        if (code === null) {
            window.location.href = "/dashboard/login";
        }

        exchangeToken(code).done(resp => {
            setToken(resp.token);
            dispatchLogin();
        }).fail((resp) => {
            window.location.href = "/dashboard/login";
        });
    } else {
        dispatchLogin();
    }
});