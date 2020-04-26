function showAlert(text, color) {
    const alert = $("#alerts").append(`
        <div class="alert alert-${color} text-wrap" role="alert">
          ${text}
        </div>
    `).children();
    setTimeout(() => alert.remove(), 3000);
}

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

function login() {
    window.localStorage.setItem("lastPage", window.location.pathname);
    window.location.href = "/dashboard/login";
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
        login();
    }

    return $.ajax({
        method: method,
        url: url,
        data: JSON.stringify(data),
        headers: {Authorization: token},
        statusCode: {
            401: logout,
            429: () => showAlert("Woah, slow down! You are sending requests too quickly.", "danger"),
            400: resp => showAlert("Error: " + resp.responseJSON.error, "danger")
        }
    });
}

function userAvatarUrl(user) {
    let url = "https://cdn.discordapp.com/";

    if (user.avatar === null) {
        url += `embed/avatars/${parseInt(user.discriminator) % 5}.png`;
    } else {
        url += `avatars/${user.id}/${user.avatar}.png`;
    }

    return url;
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
            return login();
        }

        exchangeToken(code).done(resp => {
            setToken(resp.token);
            const lastPage = window.localStorage.getItem("lastPage");
            if (lastPage !== null && lastPage !== window.location.pathname) {
                window.location.href = lastPage;
            } else {
                dispatchLogin();
            }
        }).fail((resp) => {
            return login();
        });
    } else {
        dispatchLogin();
    }
});