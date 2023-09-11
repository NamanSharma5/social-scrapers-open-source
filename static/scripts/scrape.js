document.getElementById("submit").addEventListener("click", function() {
    let username = document.getElementById("username").value;
    // navigate to page
    window.location.href = "/instagram/account/public/" + username;
    let message = document.getElementById("message");
    message.innerHTML = "Please wait...";
})