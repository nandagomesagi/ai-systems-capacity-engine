import "/assets/dependencies-ui.js";

const EMPTY_INPUT_SCHEMA = {
  type: "object",
  properties: {},
  additionalProperties: false,
};

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`;
    try {
      const body = await response.json();
      detail = body.detail || detail;
    } catch (_) {
      // Preserve the HTTP status when the body is not JSON.
    }
    throw new Error(detail);
  }
  return response.json();
}

export async function registerWebMCPTools(api) {
  const modelContext = document.modelContext || globalThis.navigator?.modelContext;
  if (!modelContext?.registerTool) {
    return {
      registered: false,
      count: 0,
      reason: "api_unavailable",
      originAgentCluster: globalThis.originAgentCluster ?? null,
    };
  }

  const controller = new AbortController();
  const registrationOptions = { signal: controller.signal };
  const tools = [
    {
      name: "get-scenario-state",
      title: "Get scenario state",
      description:
        "Return the live AI capacity scenario shown on the page, including target, explicit domain assumptions, unknown domains, and the latest engine result.",
      inputSchema: EMPTY_INPUT_SCHEMA,
      annotations: {
        readOnlyHint: true,
        untrustedContentHint: false,
      },
      execute() {
        return api.getScenarioState();
      },
    },
    {
      name: "set-scenario-target",
      title: "Set scenario target",
      description:
        "Change the live target AI infrastructure capacity and target date, update the human-visible page, and re-run the constraint engine.",
      inputSchema: {
        type: "object",
        properties: {
          target_capacity_mw: {
            type: "number",
            exclusiveMinimum: 0,
            description: "Target additional AI infrastructure capacity in megawatts.",
          },
          target_date: {
            type: "string",
            pattern: "^\\d{4}-\\d{2}-\\d{2}$",
            description: "Target date in YYYY-MM-DD format.",
          },
        },
        required: ["target_capacity_mw", "target_date"],
        additionalProperties: false,
      },
      annotations: {
        readOnlyHint: false,
        untrustedContentHint: false,
      },
      async execute(input, { signal } = {}) {
        const result = await api.setScenarioTarget(input, { signal });
        return {
          action: "target_updated",
          classification: "SCENARIO_INPUT",
          result,
        };
      },
    },
    {
      name: "set-domain-assumption",
      title: "Set domain assumption",
      description:
        "Set a hypothetical supported capacity for one required domain. The value is explicitly classified as ASSUMED, never as observed evidence. The page updates and the engine re-runs.",
      inputSchema: {
        type: "object",
        properties: {
          domain: {
            type: "string",
            enum: api.DOMAINS,
            description: "Required capacity domain to set.",
          },
          capacity_mw: {
            type: "number",
            minimum: 0,
            description: "Hypothetical supported capacity in MW.",
          },
        },
        required: ["domain", "capacity_mw"],
        additionalProperties: false,
      },
      annotations: {
        readOnlyHint: false,
        untrustedContentHint: false,
      },
      async execute(input, { signal } = {}) {
        const result = await api.setDomainAssumption(input, { signal });
        return {
          action: "domain_assumption_set",
          epistemic_state: "ASSUMED",
          domain: input.domain,
          capacity_mw: input.capacity_mw,
          result,
        };
      },
    },
    {
      name: "clear-domain-assumption",
      title: "Clear domain assumption",
      description:
        "Remove a scenario assumption for one capacity domain, restore that domain to UNKNOWN, update the page, and re-run the engine.",
      inputSchema: {
        type: "object",
        properties: {
          domain: {
            type: "string",
            enum: api.DOMAINS,
            description: "Required capacity domain to restore to UNKNOWN.",
          },
        },
        required: ["domain"],
        additionalProperties: false,
      },
      annotations: {
        readOnlyHint: false,
        untrustedContentHint: false,
      },
      async execute(input, { signal } = {}) {
        const result = await api.clearDomainAssumption(input, { signal });
        return {
          action: "domain_assumption_cleared",
          epistemic_state: "UNKNOWN",
          domain: input.domain,
          result,
        };
      },
    },
    {
      name: "evaluate-capacity",
      title: "Evaluate capacity",
      description:
        "Run the evidence-aware constraint engine against the current live scenario and update the visible result. Final deployable capacity is withheld when any required domain remains UNKNOWN.",
      inputSchema: EMPTY_INPUT_SCHEMA,
      annotations: {
        readOnlyHint: false,
        untrustedContentHint: false,
      },
      async execute(_input, { signal } = {}) {
        return api.evaluateScenario({ signal });
      },
    },
    {
      name: "get-evidence-record",
      title: "Get evidence record",
      description:
        "Retrieve one primary-source evidence record by evidence_id, including publisher, geography, claim, limitations, and source URL.",
      inputSchema: {
        type: "object",
        properties: {
          evidence_id: {
            type: "string",
            description: "Evidence identifier shown in the page evidence registry.",
          },
        },
        required: ["evidence_id"],
        additionalProperties: false,
      },
      annotations: {
        readOnlyHint: true,
        untrustedContentHint: true,
      },
      execute({ evidence_id }) {
        return api.getEvidenceRecord(evidence_id);
      },
    },
    {
      name: "trace-project-dependencies",
      title: "Trace project dependencies",
      description:
        "Trace the verified upstream dependency closure for a project graph. The current MVP graph is firehouse-grid-delivery in Loudoun County.",
      inputSchema: {
        type: "object",
        properties: {
          graph_id: {
            type: "string",
            enum: ["firehouse-grid-delivery"],
            description: "Dependency graph identifier.",
          },
        },
        required: ["graph_id"],
        additionalProperties: false,
      },
      annotations: {
        readOnlyHint: true,
        untrustedContentHint: true,
      },
      async execute({ graph_id }, { signal } = {}) {
        return fetchJson(`/api/dependencies/${encodeURIComponent(graph_id)}/trace`, { signal });
      },
    },
    {
      name: "calculate-critical-path",
      title: "Calculate critical path",
      description:
        "Evaluate timing completeness for a verified project dependency graph. A numeric total lead time is returned only when every required component lead time is evidence-supported.",
      inputSchema: {
        type: "object",
        properties: {
          graph_id: {
            type: "string",
            enum: ["firehouse-grid-delivery"],
            description: "Dependency graph identifier.",
          },
        },
        required: ["graph_id"],
        additionalProperties: false,
      },
      annotations: {
        readOnlyHint: true,
        untrustedContentHint: true,
      },
      async execute({ graph_id }, { signal } = {}) {
        return fetchJson(`/api/dependencies/${encodeURIComponent(graph_id)}/critical-path`, {
          signal,
        });
      },
    },
  ];

  let registeredCount = 0;
  try {
    for (const tool of tools) {
      await modelContext.registerTool(tool, registrationOptions);
      registeredCount += 1;
    }
  } catch (error) {
    controller.abort();
    return {
      registered: false,
      count: registeredCount,
      reason: "registration_failed",
      errorName: error?.name || "Error",
      errorMessage: error?.message || String(error),
      originAgentCluster: globalThis.originAgentCluster ?? null,
    };
  }

  // Keep the controller alive for the lifetime of the page. Aborting it
  // unregisters every tool registered with this signal.
  globalThis.__aiCapacityWebMCPController = controller;

  return {
    registered: true,
    count: tools.length,
    reason: "ok",
    originAgentCluster: globalThis.originAgentCluster ?? null,
  };
}
