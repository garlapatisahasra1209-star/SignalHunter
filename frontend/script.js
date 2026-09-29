const API_BASE_URL = "https://signalhunter.onrender.com";;

/* =========================================================
   HELPERS
   ========================================================= */

function $(selector) {
  return document.querySelector(selector);
}

function $$(selector) {
  return document.querySelectorAll(selector);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

/* =========================================================
   SAFE URL
   ========================================================= */

function getSafeSourceUrl(value) {
  const raw = String(value ?? "").trim();

  if (!raw) {
    return "";
  }

  try {
    const url = new URL(raw);

    if (
      url.protocol !== "http:" &&
      url.protocol !== "https:"
    ) {
      return "";
    }

    return url.href;
  } catch (error) {
    console.warn("Invalid source URL:", raw);
    return "";
  }
}

/* =========================================================
   TOAST
   ========================================================= */

function toast(message) {
  const stack = $("#toastStack");

  if (!stack) {
    alert(message);
    return;
  }

  const item = document.createElement("div");
  item.className = "toast";
  item.textContent = message;

  stack.appendChild(item);

  setTimeout(() => {
    item.classList.add("show");
  }, 10);

  setTimeout(() => {
    item.classList.remove("show");

    setTimeout(() => {
      item.remove();
    }, 300);
  }, 3000);
}

/* =========================================================
   SIGNAL TYPE LABEL
   ========================================================= */

function getSignalLabel(type) {
  const value = String(type || "Update").trim();

  return value
    .replace(/_/g, " ")
    .replace(/\b\w/g, letter => letter.toUpperCase());
}

/* =========================================================
   RENDER SIGNALS
   ========================================================= */

function renderSignals(signals, competitor) {
  const grid = $("#signalGrid");

  if (!grid) {
    return;
  }

  if (!signals || signals.length === 0) {
    grid.innerHTML = `
      <div class="empty-state">
        No signals found for ${escapeHtml(competitor)}.
      </div>
    `;
    return;
  }

  grid.innerHTML = signals
    .map((signal, index) => {
      const type = getSignalLabel(signal.type);
      const headline =
        signal.headline || "Untitled signal";
      const date = signal.date || "";
      const source = getSafeSourceUrl(signal.source_url);

      return `
        <article
          class="signal-card"
          data-signal-type="${escapeHtml(type.toUpperCase())}"
        >

          <div class="signal-card-top">

            <span class="signal-number">
              ${String(index + 1).padStart(2, "0")}
            </span>

            <span class="signal-type">
              ${escapeHtml(type)}
            </span>

            ${
              date
                ? `
                  <span class="signal-date">
                    ${escapeHtml(date)}
                  </span>
                `
                : ""
            }

          </div>

          <h3>
            ${escapeHtml(headline)}
          </h3>

          <div class="signal-evidence-label">
            <span>●</span>
            VERIFIED SIGNAL
          </div>

          ${
            source
              ? `
                <div class="signal-source">

                  <a
                    class="source-link"
                    href="${escapeHtml(source)}"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    View evidence source
                    <span aria-hidden="true">↗</span>
                  </a>

                </div>
              `
              : `
                <div class="signal-source">
                  <span class="source-unavailable">
                    Source unavailable
                  </span>
                </div>
              `
          }

        </article>
      `;
    })
    .join("");
}

/* =========================================================
   FORMAT AI ANALYSIS
   ========================================================= */

function formatAnalysis(analysis) {
  if (!analysis) {
    return `
      <div class="analysis-empty">
        No intelligence analysis available.
      </div>
    `;
  }

  let text = escapeHtml(analysis);

  /*
   * Remove markdown separator lines.
   */
  text = text.replace(/^[-_*]{3,}$/gm, "");

  /*
   * Main headings
   */
  text = text.replace(
    /^##\s+(.+)$/gm,
    '<div class="analysis-section-title">$1</div>'
  );

  text = text.replace(
    /^###\s+(.+)$/gm,
    '<div class="analysis-subtitle">$1</div>'
  );

  /*
   * Bold
   */
  text = text.replace(
    /\*\*(.*?)\*\*/g,
    "<strong>$1</strong>"
  );

  /*
   * Markdown table handling
   */
  const lines = text.split("\n");
  const output = [];

  let tableRows = [];
  let insideTable = false;

  function flushTable() {
    if (tableRows.length === 0) {
      return;
    }

    const rows = tableRows
      .filter(row => !/^\s*\|?\s*-+\s*\|/.test(row))
      .map(row =>
        row
          .trim()
          .replace(/^\|/, "")
          .replace(/\|$/, "")
          .split("|")
          .map(cell => cell.trim())
      );

    if (rows.length > 0) {
      const header = rows[0];

      let tableHtml = `
        <div class="intel-table-wrap">
          <table class="intel-table">
            <thead>
              <tr>
                ${header
                  .map(cell => `<th>${cell}</th>`)
                  .join("")}
              </tr>
            </thead>
            <tbody>
      `;

      rows.slice(1).forEach(row => {
        tableHtml += `
          <tr>
            ${row
              .map(cell => `<td>${cell}</td>`)
              .join("")}
          </tr>
        `;
      });

      tableHtml += `
            </tbody>
          </table>
        </div>
      `;

      output.push(tableHtml);
    }

    tableRows = [];
    insideTable = false;
  }

  for (const line of lines) {
    const trimmed = line.trim();

    if (
      trimmed.startsWith("|") &&
      trimmed.endsWith("|")
    ) {
      insideTable = true;
      tableRows.push(trimmed);
      continue;
    }

    if (insideTable) {
      flushTable();
    }

    if (!trimmed) {
      output.push("<div class='analysis-space'></div>");
      continue;
    }

    /*
     * Numbered list
     */
    const numbered = trimmed.match(
      /^(\d+)\.\s+(.+)$/
    );

    if (numbered) {
      output.push(`
        <div class="analysis-list-item">
          <span class="analysis-list-number">
            ${numbered[1]}
          </span>
          <span>${numbered[2]}</span>
        </div>
      `);

      continue;
    }

    /*
     * Bullet list
     */
    const bullet = trimmed.match(
      /^[-•*]\s+(.+)$/
    );

    if (bullet) {
      output.push(`
        <div class="analysis-bullet">
          <span>•</span>
          <span>${bullet[1]}</span>
        </div>
      `);

      continue;
    }

    /*
     * Normal paragraph
     */
    output.push(`
      <p class="analysis-paragraph">
        ${trimmed}
      </p>
    `);
  }

  flushTable();

  return output.join("");
}

/* =========================================================
   RENDER ANALYSIS
   ========================================================= */

function renderAnalysis(analysis) {
  const grid = $("#analysisGrid");

  if (!grid) {
    return;
  }

  grid.innerHTML = `
    <article class="analysis-card">

      <div class="analysis-card-header">

        <div class="analysis-title">
          <span class="analysis-icon">✦</span>
          HUNTER INTELLIGENCE
        </div>

        <div class="analysis-live">
          <span class="live-dot"></span>
          LIVE
        </div>

      </div>

      <div class="analysis-proof-bar">

        <div class="proof-item">
          <span>✓</span>
          Source-backed
        </div>

        <div class="proof-item">
          <span>✓</span>
          Evidence-linked
        </div>

        <div class="proof-item">
          <span>✓</span>
          Hindsight context
        </div>

      </div>

      <div class="analysis-text">
        ${formatAnalysis(analysis)}
      </div>

    </article>
  `;
}

/* =========================================================
   RENDER TIMELINE
   ========================================================= */

function renderTimeline(signals) {
  const timeline = $("#timelineList");

  if (!timeline) {
    return;
  }

  if (!signals || signals.length === 0) {
    timeline.innerHTML = `
      <div class="empty-state">
        No timeline data available.
      </div>
    `;
    return;
  }

  timeline.innerHTML = signals
    .map(signal => {
      const type = getSignalLabel(signal.type);

      const source = getSafeSourceUrl(
        signal.source_url
      );

      return `
        <div
          class="timeline-item"
          data-signal-type="${escapeHtml(
            type.toUpperCase()
          )}"
        >

          <div class="timeline-date">
            ${escapeHtml(
              signal.date || "Recent"
            )}
          </div>

          <div class="timeline-content">

            <span class="timeline-type">
              ${escapeHtml(type)}
            </span>

            <h3>
              ${escapeHtml(
                signal.headline || ""
              )}
            </h3>

            ${
              source
                ? `
                  <a
                    href="${escapeHtml(source)}"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="timeline-source"
                  >
                    Evidence ↗
                  </a>
                `
                : ""
            }

          </div>

        </div>
      `;
    })
    .join("");
}

/* =========================================================
   UPDATE DASHBOARD
   ========================================================= */

function updateDashboard(result) {
  const competitor =
    result.competitor || "NVIDIA";

  const signals =
    result.signals || [];

  const analysis =
    result.analysis || "";

  /*
   * Competitor
   */
  const signalsCompetitor =
    $("#signalsCompetitor");

  if (signalsCompetitor) {
    signalsCompetitor.textContent =
      competitor;
  }

  /*
   * Signal count
   */
  const countBadge =
    $(".count-badge");

  if (countBadge) {
    countBadge.textContent =
      String(signals.length).padStart(2, "0");
  }

  /*
   * Signals
   */
  renderSignals(
    signals,
    competitor
  );

  /*
   * AI analysis
   */
  renderAnalysis(
    analysis
  );

  /*
   * Timeline
   */
  renderTimeline(
    signals
  );

  /*
   * Hindsight memory
   */
  const memoriesCount =
    $("#memoriesCount");

  if (memoriesCount) {
    if (
      result.recalled_memory &&
      !result.recalled_memory.error
    ) {
      memoriesCount.textContent = "✓";
    } else {
      memoriesCount.textContent = "—";
    }
  }
}

/* =========================================================
   BACKEND API
   ========================================================= */

async function analyzeCompetitor(competitor) {
  const response = await fetch(
    `${API_BASE_URL}/analyze`,
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify({
        competitor
      })
    }
  );

  if (!response.ok) {
    let message =
      "Analysis unavailable.";

    try {
      const errorData =
        await response.json();

      message =
        errorData.detail ||
        message;
    } catch (_) {}

    throw new Error(message);
  }

  return response.json();
}

/* =========================================================
   ANALYZE BUTTON
   ========================================================= */

async function analysisSequence() {
  const button =
    $("#analyzeBtn");

  const status =
    $("#analysisStatus");

  const competitorSelect =
    $("#competitor");

  if (!competitorSelect) {
    toast(
      "Competitor selector not found."
    );
    return;
  }

  const competitor =
    competitorSelect.value.trim();

  if (!competitor) {
    toast(
      "Please select a competitor."
    );
    return;
  }

  /*
   * Disable button
   */
  if (button) {
    button.disabled = true;
  }

  /*
   * Status
   */
  if (status) {
    status.hidden = false;
    status.textContent =
      "COLLECTING VERIFIED SIGNALS";
  }

  try {
    await new Promise(resolve =>
      setTimeout(resolve, 500)
    );

    if (status) {
      status.textContent =
        "RECALLING HINDSIGHT MEMORY";
    }

    await new Promise(resolve =>
      setTimeout(resolve, 500)
    );

    if (status) {
      status.textContent =
        "GENERATING STRATEGIC ANALYSIS";
    }

    /*
     * Backend
     */
    const result =
      await analyzeCompetitor(
        competitor
      );

    if (status) {
      status.textContent =
        "UPDATING INTELLIGENCE DASHBOARD";
    }

    await new Promise(resolve =>
      setTimeout(resolve, 400)
    );

    /*
     * Update UI
     */
    updateDashboard(result);

    if (status) {
      status.textContent =
        "ANALYSIS COMPLETE";
    }

    toast(
      `${result.signals_found || 0} signals analyzed successfully.`
    );

    /*
     * Scroll to analysis
     */
    const analysis =
      $("#analysis");

    if (analysis) {
      analysis.scrollIntoView({
        behavior: "smooth"
      });
    }

  } catch (error) {
    console.error(
      "SignalHunter error:",
      error
    );

    if (status) {
      status.hidden = false;
      status.textContent =
        "ANALYSIS FAILED";
    }

    toast(
      error.message ||
      "Could not connect to backend."
    );

  } finally {
    if (button) {
      button.disabled = false;
    }
  }
}

/* =========================================================
   CHARACTER COUNTER
   ========================================================= */

const signalInput =
  $("#signalInput");

const charCount =
  $("#charCount");

if (
  signalInput &&
  charCount
) {
  signalInput.addEventListener(
    "input",
    () => {
      charCount.textContent =
        signalInput.value.length;
    }
  );
}

/* =========================================================
   ANALYZE BUTTON EVENT
   ========================================================= */

const analyzeBtn =
  $("#analyzeBtn");

if (analyzeBtn) {
  analyzeBtn.addEventListener(
    "click",
    analysisSequence
  );
}

/* =========================================================
   COMPETITOR CHANGE
   ========================================================= */

const competitor =
  $("#competitor");

if (competitor) {
  competitor.addEventListener(
    "change",
    () => {
      const name =
        competitor.value;

      const signalsCompetitor =
        $("#signalsCompetitor");

      if (signalsCompetitor) {
        signalsCompetitor.textContent =
          name;
      }
    }
  );
}

/* =========================================================
   COLLECT SIGNALS
   ========================================================= */

const collectBtn =
  $("#collectBtn");

if (collectBtn) {
  collectBtn.addEventListener(
    "click",
    () => {
      toast(
        "Latest signal collection will run through the scraper."
      );
    }
  );
}

/* =========================================================
   ADD COMPETITOR
   ========================================================= */

const addCompetitor =
  $("#addCompetitor");

if (addCompetitor) {
  addCompetitor.addEventListener(
    "click",
    () => {
      toast(
        "Competitor management will be connected next."
      );
    }
  );
}

/* =========================================================
   SUPPORTING MEMORIES
   ========================================================= */

const supportingBtn =
  $("#supportingBtn");

if (supportingBtn) {
  supportingBtn.addEventListener(
    "click",
    () => {
      const memory =
        $("#memory");

      if (memory) {
        memory.scrollIntoView({
          behavior: "smooth"
        });
      }
    }
  );
}

/* =========================================================
   NAVIGATION
   ========================================================= */

$$(".nav-item").forEach(
  button => {
    button.addEventListener(
      "click",
      () => {
        const sectionName =
          button.dataset.section;

        const section =
          document.getElementById(
            sectionName
          );

        if (section) {
          section.scrollIntoView({
            behavior: "smooth"
          });
        }
      }
    );
  }
);

/* =========================================================
   TIMELINE FILTERS
   ========================================================= */

$$(".filter").forEach(
  filter => {
    filter.addEventListener(
      "click",
      () => {

        $$(".filter").forEach(
          item =>
            item.classList.remove(
              "active"
            )
        );

        filter.classList.add(
          "active"
        );

        const filterType =
          (
            filter.dataset.filter ||
            "all"
          ).toUpperCase();

        /*
         * Signal cards
         */
        const cards =
          $$("#signalGrid .signal-card");

        cards.forEach(card => {

          if (
            filterType === "ALL"
          ) {
            card.style.display = "";
            return;
          }

          const type =
            (
              card.dataset.signalType ||
              ""
            ).toUpperCase();

          card.style.display =
            type.includes(filterType)
              ? ""
              : "none";
        });

        /*
         * Timeline
         */
        const timelineItems =
          $$("#timelineList .timeline-item");

        timelineItems.forEach(item => {

          if (
            filterType === "ALL"
          ) {
            item.style.display = "";
            return;
          }

          const type =
            (
              item.dataset.signalType ||
              ""
            ).toUpperCase();

          item.style.display =
            type.includes(filterType)
              ? ""
              : "none";
        });
      }
    );
  }
);

/* =========================================================
   SEARCH
   ========================================================= */

const searchBtn =
  $("#searchBtn");

const searchOverlay =
  $("#searchOverlay");

const closeSearch =
  $("#closeSearch");

if (
  searchBtn &&
  searchOverlay
) {
  searchBtn.addEventListener(
    "click",
    () => {

      searchOverlay.classList.add(
        "active"
      );

      searchOverlay.setAttribute(
        "aria-hidden",
        "false"
      );

      $("#searchInput")?.focus();
    }
  );
}

if (
  closeSearch &&
  searchOverlay
) {
  closeSearch.addEventListener(
    "click",
    () => {

      searchOverlay.classList.remove(
        "active"
      );

      searchOverlay.setAttribute(
        "aria-hidden",
        "true"
      );
    }
  );
}

/* =========================================================
   SEARCH WITH ESCAPE KEY
   ========================================================= */

document.addEventListener(
  "keydown",
  event => {

    if (
      event.key === "Escape" &&
      searchOverlay
    ) {
      searchOverlay.classList.remove(
        "active"
      );

      searchOverlay.setAttribute(
        "aria-hidden",
        "true"
      );
    }
  }
);

/* =========================================================
   MOBILE MENU
   ========================================================= */

const menuBtn =
  $("#menuBtn");

const sidebar =
  $("#sidebar");

if (
  menuBtn &&
  sidebar
) {
  menuBtn.addEventListener(
    "click",
    () => {
      sidebar.classList.toggle(
        "open"
      );
    }
  );
}

/* =========================================================
   INITIAL PAGE STATE
   ========================================================= */

document.addEventListener(
  "DOMContentLoaded",
  () => {

    const competitor =
      $("#competitor");

    const signalsCompetitor =
      $("#signalsCompetitor");

    if (
      competitor &&
      signalsCompetitor
    ) {
      signalsCompetitor.textContent =
        competitor.value;
    }
  }
);

/* =========================================================
   GLOBAL EXPORT
   ========================================================= */

window.SignalHunter = {
  API_BASE_URL,
  analyzeCompetitor,
  analysisSequence,
  renderSignals,
  renderAnalysis,
  renderTimeline,
  updateDashboard
};