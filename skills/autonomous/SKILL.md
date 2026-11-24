---
name: autonomous
description: Run a task through a six-agent plan → review → implement → verify loop with fixed escalation gates, so work proceeds unattended but stops at the right moments. Use when the operator hands over a multi-step task to run autonomously, says "run this loop", "do this autonomously", "go until you need me", or invokes /autonomous. Built for changes to live systems where a wrong result ships silently.
---

# Autonomous loop

Six agents, four judge gates, one batched approval. The operator is interrupted **once** — or when a
fixed trigger fires — never at every step.

The design rests on one observation: **reviews catch bad plans; only measurement catches a check that
reports green while looking at the wrong object.** Every gate below exists to separate the person who
built a thing from the person who says it works.

## The roster

| | Model tier | Job | Must NOT see |
|---|---|---|---|
| **A1** | Strong | Plans the task independently | A2's plan |
| **A2** | Strong | Plans the task independently | A1's plan |
| **A3** | Strongest | Consolidates both plans, writes the acceptance criteria, then implements | — |
| **A4** | Strongest | Attacks the plan; later checks the implementation against **A1 and A2's original briefs** | — |
| **A5** | Strong | Verifies: measures the real artefacts against the sealed criteria | **A3's reasoning or code narrative** |
| **A6** | Strong | Judge: reads state against a fixed trigger list, answers only "does this need the operator?" | — |

Use your most capable model where the table says *Strongest* (A3 builds, A4 attacks), and a strong
model elsewhere. Launch A1 and A2 in one message so they run concurrently and cannot influence each other.

## The sequence

1. **PLAN** — A1 and A2 independently. Give both the same brief; neither sees the other.
2. **CONSOLIDATE** — A3 merges them **and writes the acceptance criteria**. If it needs more from A1 or
   A2, it may go back (max 2 rounds). → **JUDGE**
3. **ADVERSARIAL REVIEW** — A4 attacks the plan *and signs off the acceptance criteria specifically*.
   Changes → back to A3 (max 2 rounds). → **SEAL**: hash the criteria document. It cannot change after
   this point. → **JUDGE**
4. **IMPLEMENT** — A3 builds **candidates only**. No writes to any live file, ever, at this stage. → **JUDGE**
5. **VERIFY** — A5 measures the real artefacts against the sealed criteria. Fails → back to step 4
   (max 2 rounds).
6. **REVIEW IMPLEMENTATION** — A1 + A2 + A4. A4 checks against the **original briefs**, not A3's
   consolidation. Fixes → back to step 4 (max 2 rounds). → **JUDGE**
7. **BATCH** — accumulate every live change into one diff bundle covering the whole task set.
8. **OPERATOR APPROVAL** — always a stop, never skipped.
9. **PROMOTE** — one window. Then post-promotion verification.

## The rules that make it work

**Acceptance criteria are written before implementation and sealed.** A loop that ends at "run the
results" invites another lap whenever results disappoint — fix, re-read, fix, re-read until the number
comes back. That is how a harness gets tuned into agreement with a wrong answer. Write what counts as
success first, have the adversary sign off *those criteria*, hash the document, and have the runner
verify the hash and refuse to run if it moved.

**Test mechanics, not outcomes, wherever possible.** "Did coverage rise", "do two machines produce
byte-identical files", "does the feed stop rewriting its history" are unambiguous and cannot be gamed.
"Did performance improve" can always be re-litigated.

**A5 gets the criteria and the objects — nothing else.** If the verifier reads the implementer's
account of what was built, it grades the story rather than the artefact.

**Every check A5 writes must be shown to fail.** Plant a deliberate defect and confirm the check goes
red before accepting any pass. A check that has never fired proves nothing about what it did not find.

**A4 reviews the implementation against the original briefs.** Otherwise a flaw shared by A3's plan and
A3's code passes unnoticed, because the reviewer is checking against the flawed plan.

**Merging must be provably complete, and this is a LIST COMPARISON, not a review.** When A3 merges
several inputs into one output, it must publish a table with one row per item in EVERY input, and each
row must land in exactly one of: KEPT (with its id in the output), MERGED INTO (naming which), or
DROPPED (with the reason). Anything in none of those columns is a silent loss.
This rule exists because it has already failed: a consolidator reported it had "kept" the single
strongest criterion its planners wrote — the one that would have caught a hand-patch whose every
changed row sat inside the training data — and had not. A grep for the criterion returned zero hits.
Re-reading by eye cannot catch this: two reviewers reading the same merged document miss the same
absence, because absence is invisible. Only enumerating the SOURCES and diffing against the OUTPUT
finds it. Make A4 check that table against the source documents, not against A3's account of them.

**Two rounds, then escalate.** The danger is not ping-pong. It is two agents quietly converging on the
same wrong premise and reporting agreement.

**Before sealing, run the criteria against the UNCHANGED system — the t=0 satisfiability sweep.**
Execute every present-state assertion the criteria make (constants, "file X equals sha Y", "both hosts
agree", any invariant about how the world is *now*) against the live system before anything has been
built. Every one must be GREEN at t=0, because the batch has not changed anything yet. Anything RED is
either a pre-existing finding you have just discovered, or a false criterion — and both must be
resolved before the hash is taken.
This exists because a criterion demanding two hosts' files be byte-identical was sealed, signed off by
an adversary twice, and was FALSE ON DAY ZERO: the two files differed by one timestamp line. It would
have gone red on a correct implementation, and it made a blocker undischargeable. The t=0 sweep catches
that in one pass, with no judgement involved.
It is the exact analogue of the completeness table: **the table proves the merge lost nothing; the t=0
run proves the file asserts nothing false about the world it seals over.**
Two supporting rules, both grep-checkable:
  - Every constant carries the host or source it was measured on.
  - Any criterion comparing host X to a constant must cite a constant measured ON HOST X. A value
    measured in one place and asserted everywhere is the defect this catches.
Generalise it where you can: run every arm that CAN be run before sealing. A criterion nobody has ever
executed is a hypothesis, not a check.

**The sweep must run every PLANTED DEFECT ARM too, not just the present-state assertions.**
This is the same rule pointed at the other half of the document, and it was learned expensively: one
batch sealed 45 criteria after a clean t=0 sweep, and implementation then found EIGHT defects, SIX of
them in the defect arms — the arms whose entire job is to prove a check is capable of failing. (A ninth
was claimed and an adversary REFUTED it: the implementer had tried the one serialisation variant that
happens to be a no-op and generalised from it. Send every such claim to an adversary before believing
it — the cost of a wrong "the seal is broken" is far higher than a wrong "run it properly".) FIVE of
the six were measured to be literally incapable of discriminating:
  - a "planted defect" that raised for the correct input too, so it distinguished nothing;
  - an in-window control planted in a fold the run does not build, so it always returned zero;
  - a `dev_cap=None` arm that produced a byte-identical panel, because the builder bounded rows anyway;
  - a falsifier whose "it halts" was already true of the unmodified control at the date it named, so
    both arms exited 1 and the demonstration proved nothing;
  - a defect arm whose control input the loader rejected identically to the defect input, so it
    distinguished nothing while appearing to raise correctly.
The positive legs had all been verified. The negative legs had never been run. A check that has never
fired and a check that CANNOT fire are indistinguishable on paper and identical in effect — and the
second is worse, because it is invisible forever.
Two corollaries, both cheap:
  - Where a defect arm carries a PRE-RECORDED baseline ("22 symbols, deepest breach 2025-06-16"),
    reproduce that baseline BEFORE sealing. A conjunctive defect clause whose second conjunct has never
    been re-measured will fail on correct code, and the implementer then cannot tell a real
    contradiction from a stale number.
  - Where a ruling's written rationale quotes a magnitude ("22 rows of 1,940,133"), measure it before
    sealing. That batch's true figure was 1,569 rows — 71x — and the decision had been taken partly on
    the smallness of the number.

**Batch the diffs.** Candidates accumulate; the operator sees one bundle, approves once, and there is
one promotion window. Staging to a scratch path on a remote host is not a live write — but say so
explicitly when you do it.

## The judge

A6 runs at **every** gate, not once, because escalation conditions do not arrive on schedule: a blocked
precondition surfaces at plan time, a contradiction at verify time, non-convergence inside a loop.

It evaluates a **fixed written trigger list**, not its own judgement — so a persuasive plan cannot talk
it round. Its only outputs are `PROCEED` and `PAUSE + reason`. It has no authority to change anything.

### Pause triggers — fixed, not judged

- **IRREVERSIBLE** — any write to a live file, on any host · anything outward-facing · anything that spends money
- **CONTRADICTION** — any result that contradicts something already reported to the operator, including by you, earlier
- **BLOCKED** — any precondition that comes back unmet
- **SPENT WINDOW** — any read of a hold-out or already-spent evaluation period, for any reason
- **NO CONVERGENCE** — two failed rounds at any loop
- **SCOPE** — anything the sealed plan did not describe

Add task-specific triggers at the start and write them down before launching A1 and A2.

## Reporting

At every pause, and at the batched approval, report in the `/summary` format: one-line BLUF, findings
graded 🔴🟠🟡🟢, every claim tagged ✔verified / ◐reported / ?assumed, a recommendation that names the
alternative you rejected, and one line of state of play. Never relay agent transcripts — synthesise.

While running, stay quiet. The point of the loop is that the operator is not interrupted.

## Before launching

Write down, in a file the agents can read: the task scope, the pause triggers, the loop limits, and any
standing constraints of the environment (blackout windows, hosts that must stay read-only, things that
must never be run). Agents cannot honour a constraint nobody wrote down.
