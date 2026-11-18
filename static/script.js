document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("claimSearch");
    const table = document.getElementById("claimsTable");

    if (searchInput && table) {
        searchInput.addEventListener("input", () => {
            const query = searchInput.value.toLowerCase();
            table.querySelectorAll("tbody tr").forEach(row => {
                row.hidden = !row.textContent.toLowerCase().includes(query);
            });
        });
    }

    const claimForm = document.getElementById("claimForm");
    if (claimForm) {
        claimForm.addEventListener("submit", event => {
            const amount = Number(claimForm.elements.claim_amount.value);
            if (!Number.isFinite(amount) || amount <= 0) {
                event.preventDefault();
                alert("Enter a claim amount greater than zero.");
            }
        });
    }
});
