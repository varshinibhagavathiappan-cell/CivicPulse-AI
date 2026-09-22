const reportEl = document.getElementById("report");
const analyzeBtn = document.getElementById("analyzeBtn");
const demoBtn = document.getElementById("demoBtn");
const loading = document.getElementById("loading");
const errorBox = document.getElementById("error");
const reportView = document.getElementById("reportView");

demoBtn.addEventListener("click", async () => {
  reportEl.value = "A resident reports that a main road near a school has a large pothole filled with water. Several two-wheelers have nearly lost control. The report says the road is heavily used during school drop-off and pickup. No injuries are reported. The exact depth of the pothole is unknown.";
  await analyze(true);
});

analyzeBtn.addEventListener("click", () => analyze(false));

async function analyze(isDemo) {
  const report = reportEl.value.trim();
  if (!report && !isDemo) {
    showError("Please describe a real-world incident first.");
    return;
  }

  hideError();
  reportView.classList.add("hidden");
  loading.classList.remove("hidden");
  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Nemotron is analyzing...";

  try {
    const response = await fetch(
      isDemo ? "http://127.0.0.1:5000/api/demo" : "http://127.0.0.1:5000/api/analyze",
      {
        method: isDemo ? "POST" : "POST",
        headers: {"Content-Type": "application/json"},
        body: isDemo ? "{}" : JSON.stringify({report})
      }
    );

    const data = await response.json();
    if (!response.ok) throw new Error(data.details || data.error || "Backend request failed.");

    render(data.result, data.model);
  } catch (err) {
    showError("Could not complete the NVIDIA AI analysis. " + err.message);
  } finally {
    loading.classList.add("hidden");
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = 'Analyze with NVIDIA AI <span>→</span>';
  }
}

function render(r, model) {
  document.getElementById("incidentType").textContent = r.incident_type || "Incident";
  document.getElementById("summary").textContent = r.summary || "No summary returned.";
  document.getElementById("department").textContent = r.department || "Needs verification";
  document.getElementById("safety").textContent = r.public_safety ? "YES — SAFETY IMPACT" : "No immediate safety impact indicated";
  document.getElementById("modelUsed").textContent = model || "NVIDIA Nemotron";

  const priority = document.getElementById("priority");
  priority.textContent = r.priority || "MEDIUM";
  priority.className = "priority " + (r.priority || "MEDIUM");

  fillList("actions", r.immediate_actions);
  fillList("resources", r.resources);
  fillList("verification", r.verification_needed);

  document.getElementById("rationale").textContent =
    r.decision_rationale || "No rationale returned.";

  const workflow = document.getElementById("workflow");
  workflow.innerHTML = "";
  (r.workflow || []).forEach((item, index) => {
    const div = document.createElement("div");
    div.className = "step";
    div.innerHTML = `
      <div class="stepno">${item.step || index + 1}</div>
      <div class="action">${escapeHtml(item.action || "")}</div>
      <div class="owner">${escapeHtml(item.owner || "Human team")}</div>
    `;
    workflow.appendChild(div);
  });

  reportView.classList.remove("hidden");
  reportView.scrollIntoView({behavior:"smooth"});
}

function fillList(id, items) {
  const ul = document.getElementById(id);
  ul.innerHTML = "";
  if (!Array.isArray(items) || !items.length) {
    const li = document.createElement("li");
    li.textContent = "No specific items returned.";
    ul.appendChild(li);
    return;
  }
  items.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    ul.appendChild(li);
  });
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, c => ({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"
  }[c]));
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove("hidden");
}

function hideError() {
  errorBox.classList.add("hidden");
}
