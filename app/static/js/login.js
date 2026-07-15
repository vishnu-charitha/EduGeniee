async function login() {

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (!email || !password) {

        alert("Please enter both email and password.");

        return;

    }

    const formData = new URLSearchParams();

    formData.append("username", email);
    formData.append("password", password);

    try {

        const response = await fetch("/auth/login", {

            method: "POST",

            headers: {

                "Content-Type": "application/x-www-form-urlencoded"

            },

            body: formData

        });

        const data = await response.json();

        if (response.ok) {

            // Save JWT Token
            localStorage.setItem("token", data.access_token);

            // Optional: Save token type
            localStorage.setItem("token_type", data.token_type);

            // Redirect to dashboard
            window.location.href = "/dashboard";

        } else {

            alert(data.detail || "Invalid email or password.");

        }

    }

    catch (error) {

        console.error(error);

        alert("Unable to connect to the server.");

    }

}