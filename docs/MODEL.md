# MODEL MVP v0.1

## Objective

The engine evaluates whether a target amount of AI infrastructure can be deployed in a region by a target date without exceeding documented physical, operational, cyber, or governance constraints.

## Minimum input

```text
location
target_capacity_mw
target_date
```

## Core entities

### Region
A geographic boundary within which capacity and constraints are evaluated.

### Resource
A capacity-bearing input such as power, grid interconnection, water, cooling, network, land, or capital.

### Infrastructure
A physical or digital system that converts resources into usable AI capacity, such as substations, transmission, data centers, cooling systems, or network links.

### Dependency
A required relation between two nodes. Dependencies carry quantity, criticality, build time, replacement time, and redundancy.

### Constraint
A requirement where available capacity may be lower than required capacity.

### Control
A cyber or governance condition required for secure deployment.

### Evidence
The source record supporting a material value or relationship.

## Resource state

Every material capacity value must distinguish:

```text
EXISTS
AVAILABLE
COMMITTED
PLANNED
ANNOUNCED
```

Every value must also carry an epistemic state:

```text
OBSERVED
DERIVED
ASSUMED
UNKNOWN
```

## Constraint calculation

For the MVP, supported deployment is calculated as the minimum supported capacity across independently required domains:

```text
DEPLOYABLE_CAPACITY = min(required_domain_support)
```

Initial domains:

```text
compute
power
grid
water
cooling
network
permits
```

The smallest supported capacity is the current binding constraint.

## Architecture gap

For each required domain:

```text
GAP = REQUIRED - AVAILABLE
```

Only positive gaps represent missing architecture.

## Secure deployability

Secure deployment is not represented as a synthetic percentage. Deployable capacity is considered secure only when all controls marked `required=true` are satisfied or explicitly classified as unresolved.

Initial cyber controls:

```text
identity_control
access_control
network_segmentation
software_provenance
supply_chain_control
incident_detection
recovery
redundancy
failure_isolation
```

Initial governance controls:

```text
authority_defined
accountability_defined
auditability
logging
human_authorization
reversibility
incident_reporting
regulatory_compliance
provenance
```

## Critical path

Dependencies form a directed acyclic graph for the MVP. Each dependency may include lead time. The critical path determines the earliest feasible date at which all required architecture can be available.

Example:

```text
generation
  -> transmission
  -> substation
  -> grid connection
  -> data center
  -> compute
```

## Outputs

```text
deployable_capacity_mw
binding_constraint
architecture_gaps
unresolved_controls
critical_path
earliest_feasible_date
evidence_refs
confidence_notes
```

## Non-goals for MVP

The first release does not claim to provide:

- a global AI capacity ranking
- AGI arrival forecasts
- complete US-China strategic comparison
- investment advice
- arbitrary ethics scores
- exact capacity where public evidence is insufficient
