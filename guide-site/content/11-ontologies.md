> **The question:** How does an AI system distinguish a plausible statement from the business fact or rule that actually governs an action?

Bryan’s “ontology-aligned compute” is a thesis in the post, not a specified architecture. This chapter offers one practical interpretation: organize retrieval, tools, validation, and model routing around explicit business concepts and their relationships.

It is an engineering proposal to test. It does not establish that every business needs a knowledge graph or that adding an ontology automatically lowers cost.

## The mental model

Separate four things that are often blended together:

1. **Vocabulary:** what words such as event, session, venue, and confirmed mean.
2. **Facts:** which particular event uses which particular venue, with provenance and time.
3. **Constraints:** what a valid record must contain or satisfy.
4. **Policy:** who may read or change a record, and under what conditions.

An ontology formalizes concepts and relationships. W3C’s OWL overview describes formalized vocabularies and their semantics. That gives a principled starting point, but it does not turn an ontology into an access-control system. [OWL reference](/agentic-eng/sources/#owl)

## Build canonical identities first

For the event assistant, begin with stable identifiers and a small domain model:

```text
Organization ─organizes→ Event ─contains→ Session
                           │               │
                           │               └─hasSpeaker→ Person
                           └─takesPlaceAt→ Venue

Venue: capacity, location, availability status
Session: scheduled time, time zone, confirmation status
```

Distinguish the entity from its label. “Main Hall,” “Hall A,” and “the downtown room” may refer to the same venue—or different venues. A model can propose an entity match, but ambiguous matches need evidence or review before they become a canonical link.

Attach provenance and validity information. A venue capacity from an old marketing brochure may conflict with an approved operations record. Store where each claim came from and which source has authority for the field, rather than selecting the most fluent description.

## Structured facts and retrieval solve different jobs

Use structured queries for exact facts and relationships when those records exist. Use text retrieval for supporting explanations, policies, and historical context. Use model generation to explain and assemble—not to silently replace the source of truth.

| Mechanism | Useful for | Boundary to remember |
| --- | --- | --- |
| Relational schema | Stable records, joins, constraints, transactional updates | Meaning and provenance still need explicit design |
| Text/vector retrieval | Finding relevant passages in documents | Similarity does not establish authority or truth |
| Knowledge graph | Explicit relationships and connected queries | A graph can still contain incorrect or stale claims |
| Formal ontology | Shared semantics and logical relationships | Entailment is not record validation or permission enforcement |
| Validation rules | Checking required structure and constraints | Passing structure checks does not prove every fact is true |

A relational database with clear domain definitions may be sufficient. Add a graph or formal ontology because a concrete query, interoperability need, or reasoning task benefits—not because the word sounds more advanced.

## Reasoning is not the same as validation

OWL’s semantic framework is useful for expressing meaning and entailment. SHACL is designed to validate RDF data graphs against shapes. Use the distinction deliberately. [OWL](/agentic-eng/sources/#owl) · [SHACL](/agentic-eng/sources/#shacl)

For example, under open-world reasoning, the absence of a recorded speaker does not necessarily mean the session has no speaker. Your publishing workflow may nevertheless require a confirmed speaker field before a session can be published. That operational requirement needs an explicit validation rule.

Likewise, “only an organizer may publish a schedule” is an authorization policy. Enforce it in the service, with authenticated identity and current permissions. Describing an Organizer class in an ontology does not grant or revoke anyone’s account privileges.

## Worked example: an ambiguous venue

A request says, “Draft the event brief for the downtown launch at Main Hall.” Retrieval finds an old announcement naming Hall B, a current approved event record pointing to `venue_17`, and an unapproved draft saying attendance will be 400.

Proposed execution:

1. Resolve the event within the requester’s authorized organization.
2. Follow its approved venue relationship to `venue_17`.
3. Retrieve the current authoritative capacity and location.
4. Treat the old announcement as historical context, not the current venue assignment.
5. Mark the unapproved attendance figure as unresolved.
6. Generate the brief with source IDs and explicit unknowns.

The model still helps interpret language and write the brief. The surrounding system decides which records count and which claims remain unverified.

## Lab: turn ten business terms into a contract

Interview a hypothetical organizer or use synthetic requirements. Define ten terms, their identifiers, relationships, source of truth, allowed states, and update rules.

Create five conflicting-record scenarios. Implement deterministic lookup and validation for the important fields. Then compare two assistant variants: unrestricted document synthesis versus synthesis using canonical lookups and explicit unresolved fields.

Evaluate factual accuracy, source correctness, unnecessary tool calls, latency, and accepted-outcome cost. This tests whether the proposed semantic structure helps your workflow; it does not assume it will.

## Failure drills

Merge two similarly named venues incorrectly. Remove a required field. Present two records with different effective dates. Revoke a user’s access while keeping the ontology unchanged. Insert a model-generated summary with no provenance and verify it cannot become authoritative by accident.

## Ship gate

The system distinguishes identity, meaning, evidence, validation, and authorization. Ambiguous or stale information remains visible rather than being polished into certainty. The value of this structure is measured in [cost of cognition](/agentic-eng/chapters/cost-of-cognition/), not assumed.
