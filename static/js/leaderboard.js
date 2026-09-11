/**
 * EXCUSE.AI // Leaderboard Search and Interactive Bindings
 */

document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("leaderboardSearch");
  const cards = document.querySelectorAll(".leaderboard-item");

  if (searchInput) {
    searchInput.addEventListener("input", () => {
      const q = searchInput.value.toLowerCase();
      cards.forEach(card => {
        const text = (card.getAttribute("data-search") || "").toLowerCase();
        card.style.display = !q || text.includes(q) ? "" : "none";
      });
    });
  }

  // "Test This Excuse" in analyzer
  document.querySelectorAll(".test-excuse-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const excuse = btn.getAttribute("data-excuse");
      const situation = btn.getAttribute("data-situation") || "Other";
      if (excuse) {
        sessionStorage.setItem("prefill_excuse", excuse);
        sessionStorage.setItem("prefill_situation", situation);
        window.location.href = "/";
      }
    });
  });

  // Check if home page has prefilled excuse from leaderboard
  const prefilled = sessionStorage.getItem("prefill_excuse");
  if (prefilled) {
    const input = document.getElementById("excuseInput");
    const sitSelect = document.getElementById("situationSelect");
    if (input) {
      input.value = prefilled;
      const sit = sessionStorage.getItem("prefill_situation");
      if (sitSelect && sit) sitSelect.value = sit;
      input.dispatchEvent(new Event("input"));
    }
    sessionStorage.removeItem("prefill_excuse");
    sessionStorage.removeItem("prefill_situation");
  }
});
