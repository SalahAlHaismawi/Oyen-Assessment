document.addEventListener('DOMContentLoaded', (event) => {
    const accessToken = localStorage.getItem('jwtToken');
    if (accessToken) {
        displayStoredTokenInfo();
    }
});

document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    try {
        const response = await fetch("/login/", {
            method: "POST",
            body: formData
        });
        if (!response.ok) {
            throw new Error('Login failed.');
        }
        const result = await response.json();
        // Store the JWT token in localStorage.
        localStorage.setItem('jwtToken', result.access_token);
        displayLoginSuccessToken(result.access_token);
    } catch (error) {
        console.error("Login error:", error);
        displayLoginError(error.message)
    }
});

function displayLoginSuccessToken(accessToken) {
    const loginForm = document.getElementById("loginForm");
    loginForm.innerHTML = ''; // Clear the form

    // Inform the user that login was successful without printing the token
    const successMessageDiv = document.createElement('div');
    successMessageDiv.textContent = "Login successful! Token stored for the next 30 mins";

    loginForm.appendChild(successMessageDiv);
}
function displayLoginError(errorMessage) {
    const errorDiv = document.getElementById("loginError");
    if (!errorDiv) {
        const loginForm = document.getElementById("loginForm");
        const newErrorDiv = document.createElement('div');
        newErrorDiv.id = "loginError";
        newErrorDiv.style.color = "red";
        newErrorDiv.textContent = errorMessage;
        loginForm.appendChild(newErrorDiv);
    } else {
        // update msg.
        errorDiv.textContent = errorMessage;
    }
}

function displayStoredTokenInfo() {
    const loginForm = document.getElementById("loginForm");
    loginForm.innerHTML = ''; // Clear the form to display the logout button

    // display already logged in.
    const tokenInfoDiv = document.createElement('div');
    tokenInfoDiv.textContent = "You're already logged in with a stored token.";

    // Create a logout button
    const logoutButton = document.createElement('button');
    logoutButton.textContent = 'Logout';
    logoutButton.onclick = function() {
        localStorage.removeItem('jwtToken'); // remove token on logout.
        loginForm.innerHTML = ''; // clear form to show page again.
        window.location.reload(); // Refresh the page after logout.
    };

    // Append to reflect UI Change.
    loginForm.appendChild(tokenInfoDiv);
    loginForm.appendChild(logoutButton);
}
