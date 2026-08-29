function toolResult(value) {
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(value, null, 2),
      },
    ],
  };
}

export async function registerWebMCPTools(api) {
  const modelContext = document.modelContext || globalThis.navigator?.modelContext;
  if (!modelContext?.registerTool) {
    return { registered: false, count: 0 };
  }

  const controller = new AbortController();
  const options = { signal: controller.signal };
  const tools = [
    {
      name: "get-scenario-state",
      description:
        "Return the live AI capacity scenario shown on the page, including target, explicit domain assumptions, unknown domains, and the latest engine result.",
      execute() {
        return toolResult(api.getScenarioState());
      },
    },
    {
      name: "set-scenario-target",
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
      },
      async execute(input) {
        const result = await api.setScenarioTarget(input);
        return toolResult({
          action: "target_updated",
          classification: "SCENARIO_INPUT",
          result,
        });
      },
    },
    {
      name: "set-domain-assumption",
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
      },
      async execute(input) {
        const result = await api.setDomainAssumption(input);
        return toolResult({
          action: "domain_assumption_set",
          epistemic_state: "ASSUMED",
          domain: input.domain,
          capacity_mw: input.capacity_mw,
          result,
        });
      },
    },
    {
      name: "clear-domain-assumption",
      description:
        "Remove a scenario assumption for one capacity domain, restore that domain to UNKNOWN, update the page, and re-run the engine.",
      inputSchema: {
        type: "object",
        properties: {
          domain: {
            type: "string",
            enum: api.DOMAINS,
          },
        },
        required: ["domain"],
      },
      async execute(input) {
        const result = await api.clearDomainAssumption(input);
        return toolResult({
          action: "domain_assumption_cleared",
          epistemic_state: "UNKNOWN",
          domain: input.domain,
          result,
        });
      },
    },
    {
      name: "evaluate-capacity",
      description:
        "Run the evidence-aware constraint engine against the current live scenario. Final deployable capacity is withheld when any required domain remains UNKNOWN.",
      async execute() {
        const result = await api.evaluateScenario();
        return toolResult(result);
      },
    },
    {
      name: "get-evidence-record",
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
      },
      execute({ evidence_id }) {
        return toolResult(api.getEvidenceRecord(evidence_id));
      },
    },
  ];

  for (const tool of tools) {
    await modelContext.registerTool(tool, options);
  }

  // Keep the controller alive for the lifetime of the page. Aborting it would
  // unregister every tool according to the current WebMCP lifecycle contract.
  globalThis.__aiCapacityWebMCPController = controller;

  return { registered: true, count: tools.length };
}
