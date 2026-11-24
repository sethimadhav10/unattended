---
name: deploy-audit
description: Audit a system that is about to go live, or is already live and unattended, so nothing is lost or missed. Use when taking something from "it works" to "it runs by itself with real consequences" — trading systems, schedulers, nightly pipelines, anything on a cron with money, data, or an audience downstream. Also use when inheriting a running system, before changing a live one, or when the user asks "is this foolproof / fully deployed / what could break". Produces an inventory, an ownership map, a ranked failure list, and a rollback path. Do NOT use for local scripts with no unattended execution, or for pure code review with no deployment dimension.
---

# Deploy audit

The gap between "it works" and "it runs unattended" is where money and data get lost. This
skill closes that gap by asking the questions that only matter once nobody is watching.

Every rule below was earned by a defect that shipped past someone competent.

## How to run it

Fan out read-only auditors in parallel — they cover more and they disagree usefully. Four
scopes that partition cleanly:

1. **Live flow** — what runs, when, reading what, writing what
2. **Asset inventory** — what exists where, what is authoritative, what is stale
3. **External dependencies** — what must arrive from outside, and what happens when it doesn't
4. **Adversarial** — what fails silently, what is unrecoverable

Tell every auditor: read-only, quote `file:line` as evidence, separate verified from
inferred, and say "I found nothing here" rather than padding. Then **verify their headline
claims yourself** before acting — auditors are confidently wrong in the same ways you are.

---

## 1. Inventory and ownership

- For every file that matters: who **writes** it, who **reads** it, and when. One writer
  per file. If a file has two writers, that is a bug waiting for a coincidence.
- Which machine is authoritative for each asset? Compare by hash, not by intent. "The Mac
  and the server both have it" is not the same as "they agree".
- What exists in **exactly one place**? Name it explicitly. A rebuild input on one laptop
  is a single point of failure regardless of how good the code is.
- Which files are **regenerated** by something else? A file you compare against nightly may
  be a moving target — check its mtime against the thing that writes it.

## 2. The silent-failure hunt

This is where the real defects are. Grep for and read every instance of:

- `|| echo`, `|| true`, `except: pass`, `except Exception: continue`
- a default that substitutes for missing data — `.get(k, 1.0)`, `fillna(1.0)`, `or 0`
- a check whose result is computed and never acted on
- a status push that fires unconditionally, without reading the exit code of the step it
  reports on

For each, state the concrete scenario in which it loses money or corrupts state. **A
failure that produces no alert is worse than a crash.**

**Absence detection:** if the whole thing silently stopped running, what would tell you?
If the answer is "a message that didn't arrive", that is not detection — silence must not
mean both "healthy" and "dead".

## 3. Anything that writes to the outside world

- **Idempotency.** If a request times out client-side but succeeded server-side, does a
  retry duplicate it? Use the provider's correlation/idempotency key. One row must never
  become three orders.
- **Record before you act, or record incrementally.** A ledger written after the loop means
  a mid-loop death leaves untracked side effects and a re-run repeats them.
- **The verify step must distinguish "nothing happened" from "no record of what happened".**
  Those look identical and mean opposite things.
- **Cross-system collisions.** If two systems share an account, a rate limit, or a lock,
  the *expected* state of one may be the abort condition of the other.

## 4. State integrity

- **Atomic writes**: temp file + rename. Truncate-then-write on a full disk is how a ledger
  becomes invalid JSON.
- **Can the state be rebuilt** from an authoritative external source, or is it the only copy
  of something (realised P&L, entry dates, counters)? Say which.
- **Backups**: automatic or hand-made? Check the timestamps. A backup taken one minute
  before the last edit does not contain the running code.

## 5. Growth and capacity

- Check disk **now**, and check the *rate*. Distinguish files that are **overwritten** from
  files that **accumulate** — they look the same in `du` and only one is a countdown.
- Everything that appends needs a bound. Verify `logrotate` actually covers your paths;
  usually it covers only the OS.
- **Before truncating any log, find its readers.** An append-only file is often somebody's
  input.

## 6. Verification discipline

These are the ones that most often make an audit itself wrong:

- **Verify prose against data.** A build log or README claiming data is corrected, adjusted,
  or validated is a hypothesis. Test it. Such claims are wrong often enough to assume
  nothing.
- **Prove the join before trusting the diff.** Most "these disagree" findings are a bad
  key — a timestamp against a date, two different vintages, a symbol-only match across
  years. Check the join first, every time.
- **Prove a check can fail.** A check that has never failed may be incapable of failing:
  asserting on the wrong region, printing into a swallowed buffer, or tautological. Feed it
  known-bad input and watch it fail before you believe it passes.
- **Beware the too-strict check.** A check that rejects real data is as bad as one that
  passes bad data, and it feels like rigour. When a gate fires, ask whether the *data* or
  the *gate* is wrong.
- **Same-vintage baselines.** Comparing against an artefact built weeks ago mixes your
  change with everything else that moved since. Rebuild the baseline today, from today's
  inputs, with the same code.
- **Pre-register the bar.** Before measuring, write down what result would mean success —
  and specifically what result would be *guaranteed by construction* and therefore prove
  nothing. Freeze it in a file with a timestamp.

## 7. Rollback and arming

- **How do you stop it?** There must be one command. Test it.
- **What does the kill switch failing look like?** If a clobbered switch degrades to
  dry-run, does that arrive at the same alert priority as routine traffic?
- **Is the alert channel itself tested?** If it is a single free service with no delivery
  receipt and every call is wrapped in a swallow, then its failure hides the failure of
  everything else.
- **What does the first live run look like?** Prefer a state where it can do nothing
  harmful — and confirm afterwards that it did nothing *for the right reason*, by reading
  the log rather than the absence of a complaint.

---

## Output

Produce four things:

1. **Execution map** — job → reads → writes, with schedule
2. **Ownership table** — asset → authoritative location → who writes it
3. **Ranked risks** — severity × likelihood, each with `file:line` evidence and a concrete
   failure scenario. Rank by what actually happens, not by how alarming it sounds.
4. **Recovery** — what is lost if the machine dies right now, and the ordered fix list

State plainly whether the system is **safe** (it fails in the right direction) and whether
it is **complete** (nothing is missing). Those are different questions and a system can be
the first without the second. If asked "is it foolproof", answer honestly — the value of
this skill is entirely in what it refuses to wave through.
