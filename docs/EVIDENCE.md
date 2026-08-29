# Evidence Contract

The engine is source-aware by design. A material conclusion must be traceable to evidence.

## Evidence record

```text
evidence_id
source_url
publisher
publication_date
retrieved_at
source_type
supports
quoted_value
unit
verification_status
notes
```

## Source classes

Preferred order:

1. primary source
2. official database
3. regulatory filing
4. company disclosure
5. reputable secondary source
6. estimate

## Epistemic states

Every modeled value must be labeled:

- `OBSERVED` — directly reported or measured by an authoritative source.
- `DERIVED` — calculated from observed inputs using a documented method.
- `ASSUMED` — scenario input or explicit modeling assumption.
- `UNKNOWN` — required value not supported by sufficient evidence.

## Verification states

```text
UNVERIFIED
SINGLE_SOURCE
CROSS_CHECKED
PRIMARY_CONFIRMED
STALE
CONFLICTING
```

## Rules

- Unknown values stay unknown; they are not silently imputed.
- Conflicting sources are retained and flagged rather than averaged automatically.
- Announcements are not treated as operational capacity.
- Derived values must retain references to every upstream evidence record used in the calculation.
- Time-sensitive values require `retrieved_at` and, where relevant, `publication_date`.

## Agent behavior

`verify_evidence()` should return the source chain and status supporting a requested claim, not merely a confidence score.
