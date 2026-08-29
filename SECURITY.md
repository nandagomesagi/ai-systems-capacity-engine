# Security

## MVP security boundary

The current AI Systems Capacity Engine is a public, read-mostly research workbench. It does not require user accounts, store secrets, execute user-supplied code, or connect to private infrastructure-control systems.

Scenario inputs are numeric/date values validated by the API. They are ephemeral and are not persisted by the server.

## Current controls

- typed API validation through FastAPI/Pydantic;
- no database or credential store;
- no server-side shell or code execution endpoints;
- no cross-origin API requirement;
- conservative browser response headers;
- source URLs are displayed as links but are not fetched by the backend on user request;
- unsupported evidence remains `UNKNOWN` rather than triggering autonomous external retrieval;
- GitHub CI tests uncertainty and evidence-boundary behavior;
- deployment health checks use a narrow non-sensitive endpoint.

## Data integrity is a security property

For this system, integrity includes epistemic integrity. The application must not permit an assumption to masquerade as a verified observation.

The following states remain distinct:

```text
OBSERVED
DERIVED
ASSUMED
UNKNOWN
```

Likewise:

```text
announced != funded != permitted != powered != compute-ready != operational
```

A data-path change that collapses these states should be treated as an integrity defect.

## WebMCP boundary

WebMCP tools currently operate only on the live public scenario and public evidence registry.

Mutating tools may:

- change target MW/date;
- add or clear explicit scenario assumptions;
- run the constraint model.

They may not:

- alter the repository or evidence registry;
- create infrastructure actions;
- access credentials;
- send email or messages;
- change DNS or cloud resources;
- turn an assumption into `OBSERVED` evidence.

## Deferred controls

Before adding authentication, persistent user data, private datasets, external write actions, or infrastructure-control integrations, the project should add a formal threat model covering at minimum:

- identity and authorization;
- tool-level least privilege;
- prompt/tool injection boundaries;
- provenance tampering;
- dependency and software-supply-chain risk;
- audit logging;
- rate limiting and abuse controls;
- secrets management;
- recovery and rollback;
- third-party service compromise;
- incident response.

## Reporting

Do not include credentials, tokens, private infrastructure details, or exploit payloads in public issues. Use a private reporting channel once one is published for the project.
