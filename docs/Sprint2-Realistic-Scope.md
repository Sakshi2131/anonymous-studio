# Sprint 2: Realistic Scope

**Date:** February 27, 2026  
**Team:** Group 3

## Sprint Goal
Build a working MongoDB-backed Kanban system with PII detection, audit trails, and workflow state management.

---

## Selected Issues (GitHub)

| Issue | Title | Label | Priority |
|-------|-------|-------|----------|
| #3 | PII detection with Presidio | must-have, sprint-1, sprint-2 | P0 |
| #8 | MongoDB persistence | must-have, sprint-1, sprint-2 | P0 |
| #15 | Create pipeline cards | must-have, sprint-2 | P0 |
| #16 | Move cards between stages | must-have, sprint-2 | P0 |
| #19 | View audit trail | must-have, sprint-2 | P1 |

---

## Professor Feedback to Address

### 1. **Who uploads datasets?**
**Answer:** Compliance officer uses the GUI to upload datasets (not just developers).
- Update user stories to reflect correct persona
- Issue #5 already has "compliance officer" as persona for uploads

### 2. **What will audit logs contain?**
**Answer:** Every audit log entry must include:
```json
{
  "timestamp": "ISO 8601",
  "event_type": "CARD_CREATED | STATUS_CHANGED | SESSION_ATTACHED | etc.",
  "card_id": "uuid",
  "actor": "user_id or system",
  "before_state": "previous status (if transition)",
  "after_state": "new status (if transition)",
  "metadata": {
    "session_id": "if session attached",
    "reason": "optional attestation reason"
  }
}
```

### 3. **Original + Anonymized Data Storage**
**Answer:** YES - must save both:
- `original_text`: Raw input with PII
- `anonymized_text`: Redacted/masked output
- `detected_entities`: List of what was found and changed
- This enables audit verification and rollback if needed

### 4. **Kanban Implementation Details**
**Answer:**
- **NOT building from scratch** - using React-based Kanban library OR simple column-based layout
- **Data updates:** MongoDB change streams or polling every 5s for multi-user sync
- **State management:** React context or Redux for local state + MongoDB as source of truth

---

## Technical Architecture Details

### System Components
```
┌─────────────┐
│   Browser   │
│  (React UI) │
└──────┬──────┘
       │ HTTP/REST
┌──────▼──────────────┐
│   Express Backend   │
│  - API routes       │
│  - Business logic   │
│  - Auth middleware  │
└──────┬──────────────┘
       │
   ┌───┴────┬─────────────┐
   │        │             │
┌──▼───┐ ┌─▼────────┐ ┌──▼──────┐
│ Mongo│ │ Presidio │ │ Azure   │
│  DB  │ │ (local)  │ │ AI PII  │
└──────┘ └──────────┘ └─────────┘
```

### Data Flow for Card Creation
1. User enters text in GUI
2. Presidio detects PII → saves to `sessions` collection
3. User clicks "Create Card"
4. Backend:
   - Creates card in `cards` collection
   - Links session_id to card
   - Writes CARD_CREATED to `audit_logs` collection
5. Frontend polls or receives update → re-renders board

### Data Flow for Status Transition
1. User clicks "Move Right" on card
2. Frontend validates transition rules
3. Backend:
   - Checks if transition is allowed
   - Updates card.status in MongoDB
   - Writes STATUS_CHANGED audit event with before/after
4. Frontend updates board view

---

## Out of Scope (Backlog)

Issues moved to backlog (no sprint-2 label):
- #17: Save session (part of #3)
- #18: Attach session to card (defer to Sprint 3)
- #20: Table view (should-have, not critical)
- #21: Badges (polish only)
- #2: Auth/login (explicitly deferred)
- #1, #4, #5, #6, #7, #9-14: Future sprints

---

## Definition of Done

Each issue is done when:
- [ ] Code committed to main branch
- [ ] Feature works in local environment
- [ ] MongoDB persists data correctly
- [ ] Audit events are written
- [ ] No console errors
- [ ] Basic manual testing passed

---

## Risk Assessment

**Risk:** Unresponsive teammates  
**Mitigation:** Reduced scope to 5 core issues, focused on essential functionality

**Risk:** Presidio + MongoDB + React learning curve  
**Mitigation:** Streamlit plug-and-play for PII detection, simple Kanban UI, standard Mongoose patterns

---

## Easiest TODO

**#21 – Visual Indicators for Urgency and Status** is the easiest story in the Todo column.

**Why it is the easiest:**
- It is **pure UI work** — no new API endpoints, no new MongoDB collections, no business logic
- Acceptance criteria are simple display rules: show a P0–P3 priority badge, a due date, an overdue badge when `due_date < today`, and a distinct visual for DONE status
- Once pipeline cards exist (#15), adding badges is just conditional styling in the component — a handful of lines of CSS/JSX or Streamlit `st.badge`-style markup
- Labeled `should-have`, so it does not block any other story
- Lowest risk of introducing bugs in core functionality

**Runner-up:** #19 (View Audit Trail) — a simple read-only MongoDB query to display events already written by #15/#16; however it has a hard dependency on those stories completing first.

---

## Redundant / Duplicate Stories

### Pair 1 — #1 and #19 (both are audit-log viewers)

| | #1 | #19 |
|---|---|---|
| **Title** | View a log of all PII processing and attestation activities | View the audit trail for a card |
| **Persona** | Administrator | User |
| **Scope** | System-wide audit log across all cards and PII events | Per-card ordered list of audit events |

**Overlap:** Both stories read from the same `audit_logs` collection in MongoDB and display `timestamp`, `actor`, `event_type`, and `before/after` state. Building #19 (per-card view) covers ≈ 80% of the work for #1 (global log). Recommendation: keep #19 in Sprint 2 as scoped and add a filter/remove-card-restriction variant for #1 in a later sprint — or merge #1 into #19 with a "show all" mode.

### Pair 2 — #17 and #18 (save session + attach session are two steps of one workflow)

| | #17 | #18 |
|---|---|---|
| **Title** | Save the results of a de-identification run | Attach a de-identification session to a pipeline card |
| **Acceptance criteria** | Run detection → save session to Mongo → return `session_id` | Select session → add `session_id` to card → write `SESSION_ATTACHED` audit event |

**Overlap:** #17 is a direct prerequisite of #18 — its sole output is the `session_id` that #18 immediately consumes. The two together form a single end-to-end workflow: *run PII detection → save → link to card*. They can be merged into one story to avoid two separate points of partially-done work, or #17 should be treated as a sub-task (not a standalone story) inside #18.

### Summary table

| Redundant pair | Recommendation |
|---|---|
| #1 ↔ #19 | Keep #19 in Sprint 2; convert #1 into a "global view" extension for Sprint 3 |
| #17 ↔ #18 | Merge #17 into #18 as a sub-task, or close #17 and add its acceptance criteria to #18 |

---

## Deliverables for Submission

1. Screenshot of GitHub project board with sprint-2 issues
2. Working demo with MongoDB persistence
3. Audit log visible in UI
4. Links to GitHub issues
