# Anonymous Studio - Sprint 2 Status

**Date:** February 28, 2026  
**Sprint:** Sprint 2 (Feb 27 - Mar 6, 2026)  
**Team:** Group 3

---

## Sprint Goal
Build MongoDB persistence layer and enhance PII detection UI with configuration options.

---

## Sprint 2 Scope (12 sprint-2 issues)

### Data & Backend Layer (You - 2 issues)
- **#8:** MongoDB persistence for sessions, cards, and audit logs (must-have) ← **PRIMARY FOCUS**
- **#17:** Save de-identification sessions (must-have)

### Card Management & Kanban UI (Sakshi2131 - 4 issues)
- **#15:** Create pipeline cards (must-have)
- **#20:** Table view of all cards (must-have)
- **#28:** Entity type selection (should-have)
- **#25:** Allowlist/Denylist configuration (must-have) - reassigned to ejenkins0113

### Workflow & Audit (hogansD - 3 issues)
- **#19:** View audit trail for cards (must-have)
- **#21:** Card badges (P0-P3, due dates, overdue) (should-have)
- **#26:** Detection rationale display (should-have)
- **#4:** Anonymization methods (must-have) - reassigned from you

### Configuration & Integration (ejenkins0113 - 4 issues)
- **#16:** Move cards between workflow stages (must-have)
- **#18:** Attach sessions to cards (must-have)
- **#25:** Allowlist/Denylist configuration (must-have)
- **#27:** Confidence threshold adjustment (should-have)

**Total Sprint 2: 12 issues** (8 must-have, 4 should-have)

---

## Current Status (as of Feb 28, 2026)

### ✅ Completed (Sprint 1 carryover)
- **#3:** PII detection with Presidio (Done - Streamlit demo functional)

### 🟡 In Progress
- **#8:** MongoDB integration - schema design in progress

### 📋 Todo
- All other sprint-2 issues assigned and ready

---

## Work Distribution

| Team Member | Assigned Issues | Focus Area |
|-------------|----------------|------------|
| You (51nk0r5w1m) | 3 | Database & data persistence layer |
| Sakshi2131 | 4 | Card UI & table views |
| hogansD | 3 | Audit trails & display features |
| ejenkins0113 | 4 | Workflow & configuration |

**Total:** 14 issues across 4 team members (3-4 per person)

---

## 🚨 Risk Assessment

### HIGH RISK

**Risk:** Unresponsive teammates  
**Impact:**two of the four team members historically inactive, may not deliver assigned card/UI work  
**Mitigation:**
- All card issues (#15, #16, #18-21) assigned to teammates as accountability measure
- If not completed by Mar 4, defer entire card system to Sprint 3
- Focus Sprint 2 demo on data layer only (MongoDB + PII detection working)

**Risk:** MongoDB schema complexity  
**Impact:** Audit logging, session storage, and card state need careful design  
**Mitigation:**
- Simple schema first: collections for `sessions`, `cards`, `audit_logs`
- Use Mongoose for validation
- Reference architecture in Sprint2-Realistic-Scope.md

### MEDIUM RISK

**Risk:** Integration between Streamlit (Python) and card system  
**Impact:** Streamlit runs separately from potential React/Node card UI  
**Mitigation:**
- Keep systems decoupled via MongoDB as shared data layer
- Streamlit writes sessions → MongoDB
- Card system reads from MongoDB
- No direct integration needed for Sprint 2

**Risk:** Scope creep - 12 sprint-2 issues may be too many  
**Impact:** Overcommitment leading to incomplete work  
**Mitigation:**
- Must-haves: #4, #8, #15-18, #20, #25 (8 issues)
- Should-haves: #21, #26-28 (4 issues) - can defer if needed
- Core deliverable: MongoDB + refined PII detection

---

## Technical Dependencies

**Blocked/Sequential:**
1. **#8 (MongoDB)** must complete first → enables #15, #17, #18, #19, #20
2. **#15 (Create cards)** must complete before #16 (Move cards) and #21 (Badges)
3. **#17 (Save sessions)** should complete before #18 (Attach sessions)

**Parallel Work (no blockers):**
- #4, #25, #26, #27, #28 can all be done independently

---

## Definition of Done

Sprint 2 is complete when:
- [ ] MongoDB connected and persisting data
- [ ] Sessions saved with original + anonymized text
- [ ] Audit log collection recording events
- [ ] Card CRUD operations functional
- [ ] PII detection UI has allow/deny lists, threshold, entity selection
- [ ] Basic table view showing all cards
- [ ] All code committed to main branch
- [ ] Demo runs without errors

---

## Deliverables for Professor

1. ✅ GitHub project board with sprint-2 issues organized
2. ✅ Issues assigned to team members
3. ✅ Sprint planning documentation (Sprint2-Realistic-Scope.md)
4. 🔲 Working demo with MongoDB persistence
5. 🔲 Sprint 2 retrospective (due after sprint ends)

---

## Next Steps (Immediate)

1. **Today (Feb 28):** 
   - Submit Sprint 2 planning assignment with screenshot
   - Begin MongoDB schema design
   
2. **By Mar 2:**
   - MongoDB connection working
   - Sessions collection CRUD operations
   
3. **By Mar 4:**
   - Check-in with teammates on card UI progress
   - Audit logging functional
   
4. **By Mar 6 (Sprint end):**
   - Integration testing
   - Demo preparation
   - Sprint 2 retrospective

---

## Success Metrics

**Sprint 2 will be successful if:**
- MongoDB persistence layer is production-ready
- PII detection has configurable options (threshold, allow/deny lists, entity types)
- At least 6/12 issues completed (50% minimum)
- Foundation established for Sprint 3 card workflow automation

**Stretch goal:**
- All 8 must-have issues completed
- Card system functional (if teammates deliver)
