# Phase 3 — Data Map: Done Means Done

## Objective recap

Map data entities, relationships, flows, access patterns, and storage requirements so Architecture (Phase 5) has a concrete shape to design around.

## Artifacts (must exist and be non-empty)

- `docs/planning/data-map.md` — populated from the template.
- `docs/planning/findings.md` — contains a `## Phase 3 Kickoff Research` subsection.

## Hard Gates

- [ ] **Kickoff research done**: `findings.md > ## Phase 3 Kickoff Research` lists 2–4 queries run, key deltas from training data, and link to primary sources. Time-boxed to 3–5 minutes.
- [ ] **Entity inventory**: `data-map.md > ## Entities` lists every first-class entity with a one-line definition and the lifecycle events (create/update/delete/archive).
- [ ] **Relationships**: `data-map.md > ## Relationships` describes cardinality (1:1, 1:N, N:M) and ownership for every entity pair with a relationship. Diagram or adjacency list present.
- [ ] **Flows**: `data-map.md > ## Flows` traces the end-to-end path of at least the top 3 user stories' data, naming read/write boundaries.
- [ ] **Access patterns**: `data-map.md > ## Access Patterns` enumerates the queries the system must answer (e.g. "list last 30 items for user X", "fetch item by slug"). Each is tagged read-heavy, write-heavy, or mixed.
- [ ] **Storage requirements**: `data-map.md > ## Storage` states estimated volumes, growth rate, retention policy, and privacy/PII classification per entity.
- [ ] **Identifiers & uniqueness**: primary keys, natural keys, and uniqueness constraints are declared per entity.
- [ ] **Validation & invariants**: required fields, value ranges, and cross-entity invariants are listed.
- [ ] **Open questions logged**: anything the user needs to decide (e.g. "soft delete vs. hard delete?") is tagged `NEEDS_HUMAN_DECISION` in `findings.md`.

## Soft Checks

- [ ] Indexing candidates called out based on access patterns.
- [ ] Migration / backfill considerations flagged if modifying an existing schema.
- [ ] Data lineage for derived/computed fields.

## Evidence format

Entity sections should be dense enough that Architecture can commit to table shapes without re-interviewing the user.

## Exit Signal

> "We know what data exists, how it connects, how it is read, and how it is written."

After this phase, Phase 5 can design system boundaries and APIs against a fixed data shape.
