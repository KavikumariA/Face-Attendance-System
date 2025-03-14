import React, { useEffect } from 'react';

function App() {
    // Redirect to register.html
    window.location.href = "register.html";

    // Add the event listener inside a useEffect hook
    useEffect(() => {
        const form = document.getElementById("registrationForm");

        if (form) {
            form.addEventListener("submit", async function (event) {
                event.preventDefault();

                const name = document.getElementById("name").value;
                const photo = document.getElementById("photo").files[0];

                if (!name || !photo) {
                    alert("⚠ Please enter a name and upload a photo!");
                    return;
                }

                const formData = new FormData();
                formData.append("name", name);
                formData.append("photo", photo);

                try {
                    const response = await fetch("http://localhost:5000/register", {
                        method: "POST",
                        body: formData,
                    });

                    const result = await response.json();

                    if (response.ok) {
                        alert(result.message);
                        window.location.href = "success.html"; // Redirect to a success page
                    } else {
                        alert(result.error);
                    }
                } catch (error) {
                    console.error("Error:", error);
                    alert("An error occurred while registering.");
                }
            });
        }
    }, []); // Empty dependency array ensures this runs only once after the component mounts

    return null; // Render nothing, as the redirect will happen immediately
}

export default App;