# Project Charter

## AI Systems Capacity Engine

This repository is the technical implementation of a long-horizon systems question:

> What architecture must exist for advanced AI to scale while remaining physically deployable, strategically resilient, governable, and cyber-secure?

## Core principles

### Architecture Before Amplification

Scale is not treated as feasible merely because compute demand, capital, or announcements exist. The supporting architecture must be identified first.

### Limits Before Scale

The system identifies binding constraints before accepting expansion claims.

### Evidence Before Assertion

Material claims and modeled values must retain provenance, geography, timestamp, source type, and epistemic state.

### No False Precision

The engine preserves:

```text
OBSERVED
DERIVED
ASSUMED
UNKNOWN
```

Unknown inputs are not silently converted into numeric certainty.

### State Separation

The system preserves the distinction:

```text
announced != funded != permitted != powered != compute-ready != operational
```

### Geography Is Part of the Data

A number is incomplete without its geographic boundary. Values from counties, utility service territories, transmission zones, project sites, and states are not interchangeable.

## Product boundary

The product is not:

- a news aggregator
- a trend dashboard
- an arbitrary AI readiness score
- an AGI arrival-date predictor
- an investment recommendation engine

The product is a constraint and dependency engine for AI systems capacity.

## Long-term asset

The strategic asset is a longitudinal, source-aware dependency graph of AI expansion:

```text
projects
resources
infrastructure
capacity
constraints
dependencies
controls
build times
regulations
failures
changes
```

Over time the system should be able to compare:

```text
forecast -> dependency requirements -> actual build -> delay -> cause -> revised state
```

## MVP discipline

The first implementation is deliberately narrow:

- human-facing region: Northern Virginia
- core county: Loudoun County
- power context: Dominion / PJM
- initial target year: 2030
- evidence preference: primary sources
- incomplete domains remain UNKNOWN

The MVP should prove the model, not simulate completeness.

## Expansion sequence

```text
Loudoun / Northern Virginia MVP
        ->
Virginia regional model
        ->
US strategic AI capacity
        ->
comparative national capacity and resilience
        ->
global AI dependency graph
```

Each expansion must preserve the same evidence and uncertainty rules.

## Engineering rule

A feature that makes the output look more complete but weakens traceability, uncertainty handling, or geographic integrity should not be merged.
