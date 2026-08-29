# Deployment — MVP

## Hosting target

The challenge MVP is prepared for a Render web service using the repository-root `render.yaml` Blueprint.

The deployment configuration is intentionally simple: one Python web service, no database, no secrets, and a health-check endpoint.

## Render Blueprint

```yaml
services:
  - type: web
    name: ai-systems-capacity-engine
    runtime: python
    plan: free
    buildCommand: pip install -e .
    startCommand: uvicorn ai_capacity_engine.api:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /api/health
    autoDeployTrigger: checksPass
```

Python is pinned through `.python-version`.

## Deployment sequence

1. Merge the tested WebMCP workbench branch into `main`.
2. In Render, create a new Blueprint from this GitHub repository.
3. Confirm the service configuration discovered from `render.yaml`.
4. Deploy.
5. Verify:

```text
GET /api/health -> 200
GET / -> workbench HTML
GET /api/evidence -> evidence registry
POST /api/evaluate -> constraint result
GET /api/dependencies/firehouse-grid-delivery/trace -> dependency trace
```

6. Test the live page in a WebMCP-capable browser.
7. Only after the Render service is healthy, add the custom domain.

## Custom domain

Planned public subdomain:

```text
intelligence.businessaifuture.com
```

Do not create the Cloudflare DNS record until Render displays the exact custom-domain DNS target for the service.

Then:

1. add the custom domain in Render;
2. copy the DNS target Render provides;
3. create the corresponding Cloudflare DNS record;
4. wait for domain verification and TLS issuance;
5. verify `/api/health` and the workbench from the custom domain;
6. repeat the WebMCP discovery/invocation test on the final origin.

## Deployment invariants

The deployed build must preserve:

- `UNKNOWN` values instead of fabricated capacity;
- human/agent shared scenario state;
- source and geography metadata;
- explicit `ASSUMED` labels for scenario overrides;
- dependency timing uncertainty;
- a working health endpoint.

A deployment that renders the UI but breaks these invariants is not considered releasable.
