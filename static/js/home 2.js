document.addEventListener("DOMContentLoaded", function() {
    var userType = document.getElementById("userType").value;
    var companyHomeUrl = document.getElementById("companyHomeUrl") ? document.getElementById("companyHomeUrl").value : null;
    var userHomeUrl = document.getElementById("userHomeUrl") ? document.getElementById("userHomeUrl").value : null;

    if (userType === '2' && companyHomeUrl) {
        window.location.href = companyHomeUrl;
    } else if (userHomeUrl) {
        window.location.href = userHomeUrl;
    }
});