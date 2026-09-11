/**
 * EXCUSE.AI // Dashboard & History Interactive Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("historySearch");
  const situationFilter = document.getElementById("historySituationFilter");
  const historyRows = document.querySelectorAll(".history-row");
  const reportModal = document.getElementById("reportModal");
  const closeReportModalBtn = document.getElementById("closeReportModalBtn");

  // Filter functionality
  function filterRows() {
    const query = (searchInput?.value || "").toLowerCase();
    const sit = (situationFilter?.value || "").toLowerCase();

    historyRows.forEach(row => {
      const text = (row.getAttribute("data-text") || "").toLowerCase();
      const rowSit = (row.getAttribute("data-situation") || "").toLowerCase();

      const matchesQuery = !query || text.includes(query);
      const matchesSit = !sit || sit === "all" || rowSit === sit;

      row.style.display = matchesQuery && matchesSit ? "" : "none";
    });
  }

  if (searchInput) searchInput.addEventListener("input", filterRows);
  if (situationFilter) situationFilter.addEventListener("change", filterRows);

  // View modal for history rows
  document.querySelectorAll(".view-report-btn").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      e.stopPropagation();
      const id = btn.getAttribute("data-id");
      if (!id || !reportModal) return;

      try {
        const res = await fetch(`/api/analysis/${id}`);
        const data = await res.json();
        if (data.success) {
          populateModalReport(data.analysis);
          reportModal.classList.add("active");
          SFX.playBlip(700, 0.05);
        }
      } catch (err) {
        showToast("Failed to retrieve analysis report.", "error");
      }
    });
  });

  if (closeReportModalBtn && reportModal) {
    closeReportModalBtn.addEventListener("click", () => {
      reportModal.classList.remove("active");
    });
  }

  function populateModalReport(item) {
    document.getElementById("modalExcuse").textContent = item.excuse;
    document.getElementById("modalScore").textContent = item.overall_score;
    document.getElementById("modalVerdict").textContent = item.verdict;
    document.getElementById("modalSituation").textContent = item.situation;
    document.getElementById("modalDate").textContent = item.created_at;
    document.getElementById("modalShortReason").textContent = `«${item.short_reason}»`;
    document.getElementById("modalDetailed").textContent = item.detailed_reason;
    document.getElementById("modalImproved").textContent = item.improved_excuse || "N/A";

    const metrics = [
      "believability", "creativity", "originality", "specificity",
      "plausibility", "desperation", "suspiciousness", "bullshit_level"
    ];

    metrics.forEach(m => {
      const val = item[m] ?? 0;
      const el = document.getElementById(`modal-${m}`);
      if (el) el.textContent = `${val}%`;
    });
  }
});
