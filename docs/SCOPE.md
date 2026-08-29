# MVP Scope and Geographic Boundaries

## Why this file exists

The phrase `Northern Virginia` is useful for the demo, but the underlying public datasets do not share one geographic boundary. Grid, utility, county, water, permitting, and regulatory records operate at different spatial levels.

The engine must never treat values from different boundaries as if they described the same denominator.

## MVP geographic model

### Core operational geography

**Loudoun County, Virginia**

Loudoun is the first county-level implementation because it provides dense public records for data-center land use, permitting, water planning, and specific electric load requests.

### Power and grid context

**Dominion / PJM DOM zone and Dominion Energy Virginia service territory**

These records are used as upstream regional context. They are not interchangeable with Loudoun County capacity.

### Regional context

`Northern Virginia` remains the human-facing regional label for the MVP. Regional records may include Loudoun, Fairfax, Prince William, Manassas, and other jurisdictions when a source explicitly defines them as part of its Northern region.

## Boundary rule

Every numeric observation must include a `geography` field and a `geography_type` field.

Allowed examples:

```text
county
utility_service_territory
transmission_zone
municipality
state
project_site
```

A value observed for one geography cannot be automatically converted into capacity for another geography.

Examples:

```text
DOM zone peak forecast != Loudoun available power
Dominion service-territory demand != Loudoun grid headroom
Loudoun water planning != Northern Virginia water capacity
project load request != regional deployable capacity
```

## Current MVP question

The first system demonstration remains:

> Can a specified amount of additional AI data-center load be deployed in Northern Virginia by a target date, and what must exist first?

Internally, the engine answers this by resolving each dependency against the narrowest defensible geography available.

## Current evidence strategy

1. Collect primary-source observations.
2. Record their exact geography and date.
3. Separate project-specific load from regional capacity.
4. Preserve unknowns where public evidence does not establish usable headroom.
5. Only calculate deployable capacity after required domains are geographically compatible or explicitly transformed by a documented method.

## Scope decision — v0.1

For the first real dataset:

- Loudoun County is the core county.
- Dominion/PJM records provide power-system context.
- Loudoun Water provides water-system context.
- Loudoun County provides land-use and zoning constraints.
- Virginia DEQ provides facility air-permit evidence.
- Virginia SCC provides state-level regulatory controls.

This structure is intentionally conservative. Geographic normalization is a model feature, not an assumption.
