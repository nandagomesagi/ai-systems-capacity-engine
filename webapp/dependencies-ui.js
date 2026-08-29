const GRAPH_ID = "firehouse-grid-delivery";

const byId = (id) => document.getElementById(id);

async function getJson(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
  return response.json();
}

function renderChips(container, values) {
  container.replaceChildren();
  if (!values.length) {
    const chip = document.createElement("span");
    chip.className = "chip";
    chip.textContent = "None";
    container.append(chip);
    return;
  }
  for (const value of values) {
    const chip = document.createElement("span");
    chip.className = "chip";
    chip.textContent = value;
    container.append(chip);
  }
}

async function initDependencyView() {
  try {
    const [trace, critical] = await Promise.all([
      getJson(`/api/dependencies/${GRAPH_ID}/trace`),
      getJson(`/api/dependencies/${GRAPH_ID}/critical-path`),
    ]);

    const traceList = byId("dependency-trace");
    traceList.replaceChildren();
    for (const node of trace.ordered_dependencies) {
      const item = document.createElement("div");
      item.className = "dependency-item";
      const arrow = document.createElement("span");
      arrow.textContent = "→";
      const label = document.createElement("strong");
      label.textContent = node;
      item.append(arrow, label);
      traceList.append(item);
    }

    byId("critical-duration").textContent = critical.total_lead_time_days === null
      ? "UNKNOWN"
      : `${critical.total_lead_time_days.toLocaleString()} days`;
    byId("critical-state").textContent = critical.complete ? "COMPLETE" : "INCOMPLETE";
    renderChips(byId("unknown-lead-times"), critical.unknown_lead_time_nodes);
    byId("dependency-notice").textContent = critical.interpretation;
  } catch (error) {
    byId("dependency-notice").textContent = `Dependency data unavailable: ${error.message}`;
    byId("critical-state").textContent = "UNAVAILABLE";
  }
}

initDependencyView();
