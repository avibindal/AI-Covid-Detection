document.addEventListener("DOMContentLoaded", function () {
    // Function to smoothly scroll to a section
    function scrollToSection(sectionId) {
        document.querySelector(sectionId).scrollIntoView({ behavior: "smooth" });
    }

    // Adding event listeners for navigation links
    document.querySelector("a[href='#s']").addEventListener("click", function (event) {
        event.preventDefault();
        scrollToSection("#upload_doc"); // Services
    });

    document.querySelector("a[href='#a']").addEventListener("click", function (event) {
        event.preventDefault();
        scrollToSection("#about"); // About
    });

    document.querySelector("a[href='#c']").addEventListener("click", function (event) {
        event.preventDefault();
        scrollToSection("#contact"); // Contact
    });

    // Explore Service button
    document.getElementById("btn_service").addEventListener("click", function () {
        scrollToSection("#upload_doc");
    });

document.getElementById("analyse_btn").addEventListener("click", async function(event) {
    event.preventDefault();  // Prevent default behavior

    let formData = new FormData();
    let fileInput = document.getElementById("fileInput").files[0];

    if (!fileInput) {
        alert("Please select a file to analyze!");
        return;
    }

    formData.append("file", fileInput);

    try {
        let response = await fetch("/", { method: "POST", body: formData });

        if (response.ok) {
            // Automatically trigger PDF download
            let blob = await response.blob();
            let link = document.createElement("a");
            link.href = window.URL.createObjectURL(blob);
            link.download = "prediction.pdf";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            alert("Analysis failed. Try again.");
        }
    } catch (error) {
        console.error("Error:", error);
    }
});

});