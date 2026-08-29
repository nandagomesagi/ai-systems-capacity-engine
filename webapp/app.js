import { registerWebMCPTools } from "/assets/webmcp.js";

export const DOMAINS = ["power", "grid", "water", "cooling", "network", "permits"];

const state = {
  evidence: [],
  scenario: null,
  assumptions: {},
  result: null,
};

const byId = (id) => document.getElementById(id);

function formatMw(value) {
  if (value === null || value === undefined) return "UNKNOWN";
  return `${Number(value).toLocaleString(undefined, { maximumFractionDigits: 1 })} MW`;
}

function nowLabel() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

export function logActivity(actor, message) {
  const list = byId("activity-log");
  const item = document.createElement("li");
  const strong = document.createElement("strong");
  strong.textContent = actor;
  item.append(strong, ` · ${nowLabel()} · ${message}`);
  list.prepend(item);
  while (list.children.length > 18) list.lastElementChild.remove();
}

function setStatus(id, text, kind = "") {
  const element = byId(id);
  element.textContent = text;
  element.className = `status ${kind}`.trim();
}

function currentTarget() {
  const target_capacity_mw = Number(byId("target-capacity").value);
  const target_date = byId("target-date").value;
  if (!Number.isFinite(target_capacity_mw) || target_capacity_mw <= 0) {
    throw new Error("Target capacity must be greater than zero.");
  }
  if (!target_date) throw new Error("Target date is required.");
  return { target_capacity_mw, target_date };
}

function domainInput(domain) {
  return document.querySelector(`[data-domain-input="${domain}"]`);
}

function domainState(domain) {
  return document.querySelector(`[data-domain-state="${domain}"]`);
}

function updateDomainState(domain) {
  const label = domainState(domain);
  const value = state.assumptions[domain];
  if (value === undefined || value === null) {
    label.textContent = "UNKNOWN";
    label.className = "domain-state";
  } else {
    label.textContent = "ASSUMED";
    label.className = "domain-state assumed";
  }
}

function renderDomainInputs() {
  const container = byId("domain-inputs");
  container.replaceChildren();

  for (const domain of DOMAINS) {
    const card = document.createElement("div");
    card.className = "domain-card";

    const header = document.createElement("div");
    header.className = "domain-name";

    const name = document.createElement("strong");
    name.textContent = domain;

    const status = document.createElement("span");
    status.className = "domain-state";
    status.dataset.domainState = domain;
    status.textContent = "UNKNOWN";

    const wrapper = document.createElement("div");
    wrapper.className = "input-with-unit";

    const input = document.createElement("input");
    input.type = "number";
    input.min = "0";
    input.step = "1";
    input.placeholder = "unknown";
    input.dataset.domainInput = domain;
    input.setAttribute("aria-label", `${domain} supported capacity assumption in MW`);
    input.addEventListener("input", () => {
      if (input.value === "") delete state.assumptions[domain];
      else state.assumptions[domain] = Number(input.value);
      updateDomainState(domain);
    });

    const unit = document.createElement("span");
    unit.textContent = "MW";

    header.append(name, status);
    wrapper.append(input, unit);
    card.append(header, wrapper);
    container.append(card);
  }
}

function renderResult(result) {
  byId("deployable-capacity").textContent = formatMw(result.deployable_capacity_mw);
  byId("provisional-capacity").textContent = formatMw(result.provisional_capacity_mw);
  byId("binding-constraint").textContent = result.binding_constraint
    ? result.binding_constraint.toUpperCase()
    : result.provisional_binding_constraint
      ? `${result.provisional_binding_constraint.toUpperCase()} (provisional)`
      : "UNKNOWN";
  byId("model-state").textContent = result.complete ? "COMPLETE" : "INCOMPLETE";

  const unknown = byId("unknown-domains");
  unknown.replaceChildren();
  if (!result.unknown_domains.length) {
    const chip = document.createElement("span");
    chip.className = "chip";
    chip.textContent = "None";
    unknown.append(chip);
  } else {
    for (const domain of result.unknown_domains) {
      const chip = document.createElement("span");
      chip.className = "chip";
      chip.textContent = domain;
      unknown.append(chip);
    }
  }

  const gaps = byId("architecture-gaps");
  gaps.replaceChildren();
  for (const domain of DOMAINS) {
    const row = document.createElement("div");
    row.className = "gap-row";
    const label = document.createElement("span");
    label.textContent = domain;
    const value = document.createElement("strong");
    const gap = result.architecture_gaps_mw[domain];
    value.textContent = gap === null || gap === undefined ? "UNKNOWN" : formatMw(gap);
    row.append(label, value);
    gaps.append(row);
  }

  byId("epistemic-notice").textContent = result.epistemic_notice;
}

function renderEvidence() {
  const list = byId("evidence-list");
  list.replaceChildren();
  byId("evidence-count").textContent = `${state.evidence.length} records`;

  for (const record of state.evidence) {
    const card = document.createElement("article");
    card.className = "evidence-card";

    const meta = document.createElement("div");
    meta.className = "meta";
    for (const text of [record.publisher, record.source_type, record.geography, record.epistemic_state]) {
      const span = document.createElement("span");
      span.textContent = text;
      meta.append(span);
    }

    const title = document.createElement("h3");
    title.textContent = record.evidence_id;

    const claim = document.createElement("p");
    claim.textContent = record.claim;

    const link = document.createElement("a");
    link.href = record.url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = "Open primary source";

    card.append(meta, title, claim, link);
    list.append(card);
  }
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`;
    try {
      const body = await response.json();
      detail = body.detail || detail;
    } catch (_) {
      // Keep HTTP detail when the body is not JSON.
    }
    throw new Error(detail);
  }
  return response.json();
}

export function getScenarioState() {
  const target = currentTarget();
  return {
    location: state.scenario?.location || "Northern Virginia",
    ...target,
    domain_assumptions: { ...state.assumptions },
    result: state.result,
  };
}

export async function evaluateScenario(actor = "Human") {
  const button = byId("evaluate-button");
  button.disabled = true;
  try {
    const target = currentTarget();
    const result = await fetchJson("/api/evaluate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ...target,
        domain_assumptions: state.assumptions,
      }),
    });
    state.result = result;
    renderResult(result);
    logActivity(actor, `evaluated ${target.target_capacity_mw.toLocaleString()} MW by ${target.target_date}`);
    return result;
  } finally {
    button.disabled = false;
  }
}

export async function setScenarioTarget({ target_capacity_mw, target_date }) {
  if (!Number.isFinite(target_capacity_mw) || target_capacity_mw <= 0) {
    throw new Error("target_capacity_mw must be > 0");
  }
  if (!/^\d{4}-\d{2}-\d{2}$/.test(target_date)) {
    throw new Error("target_date must use YYYY-MM-DD");
  }
  byId("target-capacity").value = String(target_capacity_mw);
  byId("target-date").value = target_date;
  logActivity("Agent", `changed target to ${target_capacity_mw.toLocaleString()} MW by ${target_date}`);
  return evaluateScenario("Agent");
}

export async function setDomainAssumption({ domain, capacity_mw }) {
  if (!DOMAINS.includes(domain)) throw new Error(`Unknown domain: ${domain}`);
  if (!Number.isFinite(capacity_mw) || capacity_mw < 0) {
    throw new Error("capacity_mw must be >= 0");
  }
  state.assumptions[domain] = capacity_mw;
  domainInput(domain).value = String(capacity_mw);
  updateDomainState(domain);
  logActivity("Agent", `set ${domain} support to ${capacity_mw.toLocaleString()} MW as ASSUMED`);
  return evaluateScenario("Agent");
}

export async function clearDomainAssumption({ domain }) {
  if (!DOMAINS.includes(domain)) throw new Error(`Unknown domain: ${domain}`);
  delete state.assumptions[domain];
  domainInput(domain).value = "";
  updateDomainState(domain);
  logActivity("Agent", `cleared ${domain}; state restored to UNKNOWN`);
  return evaluateScenario("Agent");
}

export function getEvidenceRecord(evidence_id) {
  const record = state.evidence.find((item) => item.evidence_id === evidence_id);
  if (!record) throw new Error(`Evidence record not found: ${evidence_id}`);
  return record;
}

async function init() {
  renderDomainInputs();
  byId("evaluate-button").addEventListener("click", () => {
    evaluateScenario("Human").catch((error) => {
      logActivity("System", `evaluation error: ${error.message}`);
    });
  });

  try {
    const [health, scenario, evidence] = await Promise.all([
      fetchJson("/api/health"),
      fetchJson("/api/default-scenario"),
      fetchJson("/api/evidence"),
    ]);
    setStatus("api-status", `API: ${health.status}`, "ok");
    state.scenario = scenario;
    state.evidence = evidence.records || [];
    byId("target-capacity").value = String(scenario.target_capacity_mw);
    byId("target-date").value = scenario.target_date;
    renderEvidence();
    logActivity("System", `loaded ${state.evidence.length} evidence records`);
  } catch (error) {
    setStatus("api-status", "API: unavailable", "warn");
    logActivity("System", `startup error: ${error.message}`);
    return;
  }

  await evaluateScenario("System");

  const tools = await registerWebMCPTools({
    DOMAINS,
    getScenarioState,
    setScenarioTarget,
    setDomainAssumption,
    clearDomainAssumption,
    evaluateScenario: () => evaluateScenario("Agent"),
    getEvidenceRecord,
    setStatus,
    logActivity,
  });

  if (tools.registered) {
    setStatus("webmcp-status", `WebMCP: ${tools.count} tools`, "ok");
    logActivity("System", `registered ${tools.count} WebMCP tools`);
  } else {
    setStatus("webmcp-status", "WebMCP: browser unavailable", "warn");
    logActivity("System", "WebMCP API not exposed by this browser");
  }
}

init().catch((error) => {
  setStatus("api-status", "Startup failed", "warn");
  logActivity("System", error.message);
});
