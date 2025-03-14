document.addEventListener("DOMContentLoaded", function () {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')

    for (let tooltip of tooltipTriggerList) {
        new bootstrap.Tooltip(tooltip);
    }
})