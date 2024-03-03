let logoutTimer;
function startTimers() {
    // Logout after 30 minutes of inactivity
    logoutTimer = setTimeout(logoutUser, 1800000); // 1800000=30 minutes in milliseconds
}

function resetTimers() {
    clearTimeout(logoutTimer);
    startTimers();
}

// Redirect to the logout URL, which will be handled by Django
function logoutUser() {
    window.location.href = LOGOUT_URL; // Use the dynamically defined URL
}

// Listen for any user actions
window.onload = startTimers;
document.onmousemove = resetTimers;
document.onkeydown = resetTimers;