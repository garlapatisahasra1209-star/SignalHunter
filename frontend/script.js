const API_BASE_URL = "http://localhost:8000";

const DEMO_DATA = {
  Samsung: {
    signals: [
      [
        "PRODUCT",
        "Galaxy AI Enterprise Device",
        "Samsung announces an AI-focused productivity device built for enterprise workflows.",
        "SEP 28, 2026",
        "HIGH"
      ],
      [
        "PARTNERSHIP",
        "Cloud workflow alliance",
        "A new partner ecosystem expands Samsung’s enterprise AI footprint.",
        "SEP 24, 2026",
        "HIGH"
      ],
      [
        "MARKET",
        "Enterprise AI momentum",
        "Samsung’s messaging shifts toward IT leaders and operations teams.",
        "SEP 19, 2026",
        "MEDIUM"
      ],
      [
        "PRICING",
        "Premium AI tier",
        "New premium capabilities arrive with a higher-value subscription tier.",
        "SEP 12, 2026",
        "MEDIUM"
      ],
      [
        "PRODUCT",
        "On-device intelligence",
        "Next-generation device processing keeps more AI tasks local.",
        "SEP 05, 2026",
        "HIGH"
      ],
      [
        "MARKETING",
        "Work smarter campaign",
        "Campaign creative highlights productivity outcomes over specs.",
        "AUG 29, 2026",
        "MEDIUM"
      ]
    ],

    analysis: [
      [
        "PRODUCT CHANGE",
        "▣",
        "AI productivity device",
        "The move broadens the product story beyond a consumer smartphone.",
        "OBSERVED · 94% confidence",
        false
      ],
      [
        "PRICING CHANGE",
        "◈",
        "Premium AI tier",
        "Packaging suggests willingness to monetize deeper workflows.",
        "OBSERVED · 81% confidence",
        false
      ],
      [
        "TARGET MARKET",
        "◌",
        "Consumers → Enterprise customers",
        "May indicate a broader enterprise positioning strategy.",
        "AI INTERPRETATION · 84% confidence",
        true
      ],
      [
        "MARKETING CHANGE",
        "⌁",
        "Outcome-led messaging",
        "The narrative is moving from features to measurable productivity.",
        "AI INTERPRETATION · 79% confidence",
        true
      ],
      [
        "STRATEGIC SIGNAL",
        "✦",
        "Consumer-to-enterprise expansion",
        "Multiple signals point toward a deliberate adjacency strategy.",
        "AI INTERPRETATION · 88% confidence",
        true
      ],
      [
        "IMPORTANCE",
        "!",
        "High strategic importance",
        "This may change how the category frames AI differentiation.",
        "AI INTERPRETATION · 86% confidence",
        true
      ]
    ],

    timeline: [
      [
        "SEP 05",
        "PRODUCT",
        "New AI Smartphone",
        "Premium AI features introduced on-device."
      ],
      [
        "SEP 12",
        "PRICING",
        "Pricing Update",
        "Higher-value tier added for advanced AI capabilities."
      ],
      [
        "SEP 19",
        "MARKET",
        "Enterprise Partnership",
        "New alliance opens enterprise distribution."
      ],
      [
        "SEP 28",
        "PRODUCT",
        "Enterprise AI Device",
        "AI productivity device announced for business workflows."
      ]
    ]
  },

  Apple: {
    signals: [
      [
        "PRODUCT",
        "Apple Intelligence rollout",
        "New intelligence features arrive across the latest product family.",
        "SEP 27, 2026",
        "HIGH"
      ],
      [
        "MARKETING",
        "Personal intelligence narrative",
        "Messaging emphasizes privacy and personal context.",
        "SEP 21, 2026",
        "HIGH"
      ],
      [
        "PARTNERSHIP",
        "Developer model access",
        "Developers gain new tools for contextual app experiences.",
        "SEP 16, 2026",
        "MEDIUM"
      ],
      [
        "PRICING",
        "Services bundle shift",
        "AI experiences are positioned inside the wider services ecosystem.",
        "SEP 10, 2026",
        "MEDIUM"
      ],
      [
        "TECHNOLOGY",
        "Private compute upgrade",
        "New architecture reinforces on-device intelligence.",
        "SEP 03, 2026",
        "HIGH"
      ],
      [
        "MARKET",
        "Premium AI adoption",
        "Enterprise teams are testing Apple’s private AI workflows.",
        "AUG 25, 2026",
        "MEDIUM"
      ]
    ],

    analysis: [
      [
        "PRODUCT CHANGE",
        "▣",
        "Context-aware product layer",
        "Apple is threading intelligence through existing product surfaces.",
        "OBSERVED · 93% confidence",
        false
      ],
      [
        "PRICING CHANGE",
        "◈",
        "Services-led packaging",
        "The signal may support a broader ecosystem monetization approach.",
        "AI INTERPRETATION · 76% confidence",
        true
      ],
      [
        "TARGET MARKET",
        "◌",
        "Individuals → teams",
        "Early evidence suggests a gradual move into collaborative workflows.",
        "AI INTERPRETATION · 73% confidence",
        true
      ],
      [
        "MARKETING CHANGE",
        "⌁",
        "Privacy as differentiation",
        "Private processing is becoming a strategic brand asset.",
        "OBSERVED · 91% confidence",
        false
      ],
      [
        "STRATEGIC SIGNAL",
        "✦",
        "Platform intelligence moat",
        "Multiple product surfaces may compound Apple’s distribution advantage.",
        "AI INTERPRETATION · 85% confidence",
        true
      ],
      [
        "IMPORTANCE",
        "!",
        "High strategic importance",
        "The ecosystem framing could influence category expectations.",
        "AI INTERPRETATION · 82% confidence",
        true
      ]
    ],

    timeline: [
      [
        "SEP 03",
        "TECHNOLOGY",
        "Private Compute Upgrade",
        "New architecture reinforces on-device intelligence."
      ],
      [
        "SEP 10",
        "PRICING",
        "Services Bundle Shift",
        "AI experiences move into the ecosystem bundle."
      ],
      [
        "SEP 16",
        "PARTNERSHIP",
        "Developer Model Access",
        "Developers gain tools for contextual app experiences."
      ],
      [
        "SEP 27",
        "PRODUCT",
        "Apple Intelligence Rollout",
        "Intelligence features arrive across the product family."
      ]
    ]
  },

  Google: {
    signals: [
      [
        "TECHNOLOGY",
        "Agentic Workspace update",
        "Google adds autonomous assistance to core productivity workflows.",
        "SEP 26, 2026",
        "HIGH"
      ],
      [
        "PRODUCT",
        "Gemini device integration",
        "New device experiences make the model layer more ambient.",
        "SEP 20, 2026",
        "HIGH"
      ],
      [
        "MARKET",
        "AI-native operations",
        "Enterprise teams receive new workflow automation tools.",
        "SEP 15, 2026",
        "MEDIUM"
      ],
      [
        "PARTNERSHIP",
        "Cloud model program",
        "Partners can deploy specialized agents through Google Cloud.",
        "SEP 09, 2026",
        "MEDIUM"
      ],
      [
        "PRICING",
        "Workspace AI tier",
        "Advanced agents are grouped into a new business tier.",
        "SEP 02, 2026",
        "MEDIUM"
      ],
      [
        "MARKETING",
        "The agent era",
        "Messaging shifts from answers to delegated action.",
        "AUG 26, 2026",
        "HIGH"
      ]
    ],

    analysis: [
      [
        "PRODUCT CHANGE",
        "▣",
        "Agentic workflow layer",
        "The product is evolving from assistant toward delegated action.",
        "OBSERVED · 95% confidence",
        false
      ],
      [
        "PRICING CHANGE",
        "◈",
        "Business tier expansion",
        "Packaging shows a clearer path to enterprise monetization.",
        "OBSERVED · 82% confidence",
        false
      ],
      [
        "TARGET MARKET",
        "◌",
        "Teams → operations",
        "May indicate an ambition to own higher-value workflows.",
        "AI INTERPRETATION · 83% confidence",
        true
      ],
      [
        "MARKETING CHANGE",
        "⌁",
        "Answers → action",
        "The narrative is moving toward measurable task completion.",
        "AI INTERPRETATION · 90% confidence",
        true
      ],
      [
        "STRATEGIC SIGNAL",
        "✦",
        "Workflow ownership",
        "The pattern appears to connect models, cloud, and distribution.",
        "AI INTERPRETATION · 86% confidence",
        true
      ],
      [
        "IMPORTANCE",
        "!",
        "High strategic importance",
        "A change in the unit of value may pressure adjacent platforms.",
        "AI INTERPRETATION · 84% confidence",
        true
      ]
    ],

    timeline: [
      [
        "AUG 26",
        "MARKETING",
        "The Agent Era",
        "Messaging shifts from answers to delegated action."
      ],
      [
        "SEP 02",
        "PRICING",
        "Workspace AI Tier",
        "Advanced agents grouped into a business tier."
      ],
      [
        "SEP 15",
        "MARKET",
        "AI-native Operations",
        "New workflow automation tools for enterprise teams."
      ],
      [
        "SEP 26",
        "TECHNOLOGY",
        "Agentic Workspace Update",
        "Autonomous assistance lands in productivity workflows."
      ]
    ]
  }
};


const $ = (selector, root = document) =>
  root.querySelector(selector);

const $$ = (selector, root = document) =>
  [...root.querySelectorAll(selector)];


let selectedCompetitor = "Samsung";


function renderSignals(name = selectedCompetitor) {

  const data = DEMO_DATA[name];

  if (!data) return;

  $("#signalsCompetitor").textContent = name;

  $("#signalGrid").innerHTML = data.signals
    .map(
      (s, i) => `
        <article class="signal-card" data-index="${i}">

          <div class="signal-top">
            <span class="category">${s[0]}</span>
            <span class="strength">● ${s[4]}</span>
          </div>

          <h3>${s[1]}</h3>

          <p>${s[2]}</p>

          <div class="signal-foot">
            <span>${s[3]}</span>
            <span>DEMO SOURCE ↗</span>
          </div>

          <div class="expand-note">
            SignalHunter read: this observation is being compared against
            ${name}'s previous activity and related market context.
          </div>

        </article>
      `
    )
    .join("");

  $$(".signal-card").forEach((card) => {
    card.addEventListener("click", () => {
      card.classList.toggle("expanded");
    });
  });
}


function renderAnalysis(name = selectedCompetitor) {

  const data = DEMO_DATA[name];

  if (!data) return;

  $("#analysisGrid").innerHTML = data.analysis
    .map(
      (a) => `
        <article class="analysis-card ${a[5] ? "interpretation" : ""}">

          <div class="analysis-label">
            <span class="analysis-icon">${a[1]}</span>
            ${a[5] ? "AI INTERPRETATION" : "OBSERVED"}
          </div>

          <h3>${a[2]}</h3>

          <p>${a[3]}</p>

          <small>${a[4]}</small>

        </article>
      `
    )
    .join("");
}


function renderTimeline(name = selectedCompetitor, filter = "all") {

  const data = DEMO_DATA[name];

  if (!data) return;

  const items = data.timeline.filter(
    (x) => filter === "all" || x[1] === filter
  );

  $("#timelineList").innerHTML =
    items
      .map(
        (x, i) => `
          <article
            class="timeline-event"
            style="animation-delay:${i * 70}ms"
          >

            <div class="timeline-date">
              ${x[0]}
            </div>

            <div>

              <span class="category">
                ${x[1]}
              </span>

              <h3>
                ${x[2]}
              </h3>

              <p>
                ${x[3]}
              </p>

            </div>

          </article>
        `
      )
      .join("") ||
    `
      <div class="timeline-event">

        <div class="timeline-date">
          —
        </div>

        <div>

          <h3>
            No matching events
          </h3>

          <p>
            Try another timeline filter.
          </p>

        </div>

      </div>
    `;
}


function toast(message) {

  const el = document.createElement("div");

  el.className = "toast";

  el.innerHTML = `
    <b>✓</b>
    <span>${message}</span>
    <button aria-label="Close notification">
      ×
    </button>
  `;

  $("#toastStack").append(el);

  el.querySelector("button").onclick = () =>
    el.remove();

  setTimeout(() => {
    el.remove();
  }, 4800);
}


function setCompetitor(name) {

  selectedCompetitor = name;

  renderSignals();
  renderAnalysis();
  renderTimeline();

  toast(
    `${name} intelligence context loaded.`
  );
}


/* =========================================================
   ANALYSIS SEQUENCE
   Frontend-only demo behavior.
   Backend teammate can later replace this with the real API.
   ========================================================= */

function analysisSequence() {

  const status = $("#analysisStatus");

  const input = $("#signalInput");

  const competitor =
    $("#competitor").value;

  const information =
    input.value.trim();


  if (!information) {

    toast(
      "Please enter a competitor signal first."
    );

    input.focus();

    return;
  }


  const steps = [

    "01 · COLLECTING SIGNALS",

    "02 · RECALLING HINDSIGHT MEMORY",

    "03 · CONNECTING HISTORICAL CONTEXT",

    "04 · COMPARING SIGNALS",

    "05 · GENERATING STRATEGIC INSIGHT",

    "06 · UPDATING MEMORY"

  ];


  let i = 0;


  $("#analyzeBtn").disabled = true;

  $("#analyzeBtn").innerHTML =
    '<span class="button-icon">◌</span> Analyzing…';

  status.hidden = false;


  const tick = () => {

    status.innerHTML = `
      <span>
        ◌ ${steps[i]}
      </span>

      <div class="progress">
        <i></i>
      </div>
    `;


    if (i < steps.length - 1) {

      i++;

      setTimeout(
        tick,
        550
      );

    } else {

      setTimeout(() => {

        const today =
          new Date().toLocaleDateString(
            "en-US",
            {
              month: "short",
              day: "2-digit",
              year: "numeric"
            }
          ).toUpperCase();


        const signalText =
          information.length > 140
            ? information.substring(0, 140) + "…"
            : information;


        /*
          Add the user's new signal
          to the top of the signal feed.
        */

        const signalGrid =
          $("#signalGrid");


        signalGrid.insertAdjacentHTML(
          "afterbegin",

          `
            <article
              class="signal-card expanded"
              data-index="new"
            >

              <div class="signal-top">

                <span class="category">
                  NEW SIGNAL
                </span>

                <span class="strength">
                  ● HIGH
                </span>

              </div>


              <h3>
                ${competitor} — New Intelligence
              </h3>


              <p>
                ${signalText}
              </p>


              <div class="signal-foot">

                <span>
                  ${today}
                </span>

                <span>
                  USER SIGNAL ↗
                </span>

              </div>


              <div class="expand-note">

                SignalHunter read:
                this new observation is being
                compared against ${competitor}'s
                previous activity and historical context.

              </div>

            </article>
          `
        );


        /*
          Add a new AI interpretation card.
        */

        $("#analysisGrid").insertAdjacentHTML(

          "afterbegin",

          `
            <article
              class="analysis-card interpretation"
            >

              <div class="analysis-label">

                <span class="analysis-icon">
                  ✦
                </span>

                AI INTERPRETATION

              </div>


              <h3>
                Strategic Signal Detected
              </h3>


              <p>

                ${competitor} has produced
                a new signal that should be
                compared with previous activity
                to identify changes in product
                direction, market positioning
                and strategy.

              </p>


              <small>
                GENERATED FROM CURRENT SIGNAL · HIGH RELEVANCE
              </small>

            </article>
          `
        );


        /*
          Keep the competitor heading correct.
        */

        $("#signalsCompetitor").textContent =
          competitor;


        /*
          Finish the analysis animation.
        */

        status.innerHTML = `
          <span style="color:var(--success)">
            ✓ ANALYSIS COMPLETE · RESULTS UPDATED
          </span>
        `;


        $("#analyzeBtn").disabled = false;


        $("#analyzeBtn").innerHTML =
          '<span class="button-icon">✦</span> Analyze signal <span>→</span>';


        toast(
          `Analysis complete. ${competitor} signal added to the intelligence feed.`
        );


        /*
          Scroll to AI Analysis.
        */

        document
          .querySelector("#analysis")
          .scrollIntoView({
            behavior: "smooth",
            block: "start"
          });


      }, 650);
    }
  };


  tick();
}


/* =========================================================
   EVENT LISTENERS
   ========================================================= */


$("#competitor").addEventListener(
  "change",
  (e) => {

    setCompetitor(
      e.target.value
    );

  }
);


$("#signalInput").addEventListener(
  "input",
  (e) => {

    $("#charCount").textContent =
      e.target.value.length;

  }
);


$("#analyzeBtn").addEventListener(
  "click",
  () => {

    analysisSequence();

  }
);


/* =========================================================
   COLLECT SIGNAL BUTTON
   ========================================================= */

const collectBtn =
  $("#collectBtn");

if (collectBtn) {

  collectBtn.addEventListener(
    "click",
    () => {

      toast(
        `Signal collected for ${selectedCompetitor}.`
      );

    }
  );

}


/* =========================================================
   ADD COMPETITOR
   ========================================================= */

const addCompetitorBtn =
  $("#addCompetitorBtn");

if (addCompetitorBtn) {

  addCompetitorBtn.addEventListener(
    "click",
    () => {

      toast(
        "Competitor workspace ready."
      );

    }
  );

}


/* =========================================================
   SUPPORTING MEMORIES
   ========================================================= */

const memoryBtn =
  $("#supportingMemoriesBtn");

if (memoryBtn) {

  memoryBtn.addEventListener(
    "click",
    () => {

      toast(
        "Historical memory context loaded."
      );

    }
  );

}


/* =========================================================
   TIMELINE FILTERS
   ========================================================= */

$$("[data-filter]").forEach(
  (button) => {

    button.addEventListener(
      "click",
      () => {

        $$("[data-filter]").forEach(
          (item) =>
            item.classList.remove("active")
        );

        button.classList.add("active");

        const filter =
          button.dataset.filter;

        renderTimeline(
          selectedCompetitor,
          filter
        );

      }
    );

  }
);


/* =========================================================
   NAVIGATION
   ========================================================= */

$$("[data-scroll]").forEach(
  (item) => {

    item.addEventListener(
      "click",
      () => {

        const target =
          document.querySelector(
            item.dataset.scroll
          );

        if (target) {

          target.scrollIntoView({
            behavior: "smooth",
            block: "start"
          });

        }

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

const searchInput =
  $("#searchInput");

const closeSearch =
  $("#closeSearch");


if (searchBtn && searchOverlay) {

  searchBtn.addEventListener(
    "click",
    () => {

      searchOverlay.hidden = false;

      if (searchInput) {
        searchInput.focus();
      }

    }
  );

}


if (closeSearch && searchOverlay) {

  closeSearch.addEventListener(
    "click",
    () => {

      searchOverlay.hidden = true;

    }
  );

}


/* =========================================================
   MENU BUTTON
   ========================================================= */

const menuBtn =
  $("#menuBtn");

const sidebar =
  $(".sidebar");


if (menuBtn && sidebar) {

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
   INITIAL RENDER
   ========================================================= */

renderSignals();

renderAnalysis();

renderTimeline();


/* =========================================================
   BACKEND API FUNCTION
   Your teammate can use this later.
   ========================================================= */

async function analyzeCompetitor(
  competitor,
  information
) {

  const response =
    await fetch(
      `${API_BASE_URL}/analyze`,
      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json"
        },

        body: JSON.stringify({
          competitor,
          information
        })
      }
    );


  if (!response.ok) {

    throw new Error(
      "analysis unavailable"
    );

  }


  return response.json();

}


/* =========================================================
   PUBLIC SIGNALHUNTER OBJECT
   ========================================================= */

window.SignalHunter = {

  API_BASE_URL,

  DEMO_DATA,

  analyzeCompetitor

};