---
name: ship-safe
description: Use before changing, verifying, or promoting anything that runs unattended with real consequences — trading systems, nightly pipelines, live data feeds, anything where a wrong number ships silently. Enforces the review discipline that catches "a check reporting GREEN while looking at the wrong thing". Use when writing a verification, when a check passes and you are about to believe it, before any irreversible or live write, and when a repair is declared done.
---

# Ship-safe

This exists because of one repeated failure, observed eight times in one programme:

> **A check reported GREEN while looking at the wrong thing.**

Not wrong logic. Wrong *object*. Every instance passed its own test.

The catalogue, because the shapes repeat:

1. A parity gate hashed the code and the model, never the data. Identical hash, hollowed inputs, three months.
2. A coverage gate measured the right number and was exempted by name in writing. Nobody came back.
3. A completeness check read the file it had just written. `rows == n` held by construction.
4. Documents landed in a directory the parser did not glob. The crawl exited green on nothing.
5. A cross-host consistency gate passed because both hosts read the same missing data. Agreement on garbage.
6. A permanent billing failure was classified as a transient token error and retried 5,334 times. A retry loop reads as "still working" from every angle except the one nobody checked.
7. A fix printed `adjusted N rows` while every consumer read a stale reference to the pre-fix data. The count was real; the effect was zero.
8. A verification asserted on the source column. The model read a *derived* column, where the null had already become a zero.

## The rules

### 1. Assert where the value is consumed, not where it is produced
Instance 8. The source file was correct and irrelevant. Trace the value to the last point before it is
used for a decision, and assert **there**. If a fix is meant to reach a model, the assertion belongs on
the model's input, not on the file three steps upstream.

### 2. Verification must call the real code, never re-implement it
Instance 8's root cause. A verification script contained one line the real system did not have, and
reported 100% success about code that does not exist. Import the real function. If it cannot be
imported, that is a finding about the system, not a licence to copy the logic.

### 3. Every check must be shown capable of failing
Instances 3 and 5. Before trusting a PASS, break the input on purpose and confirm the check goes RED.
A check validated against the same object that produced the result cannot fail — that is not a check,
it is a restatement. Negative controls are as load-bearing as positive ones.

### 4. A positive control must fire on the real defect, not on the mechanism
Proving a gate CAN fire is not proving it fires on the actual fault. Point controls at the specific
rows the defect was diagnosed from, at a date where it genuinely manifests — not at an edge where the
condition has already lapsed.

### 5. Two independent reviewers before anything irreversible, on different angles
One hunting **mechanism** (is the diagnosis right, is the maths right, is the option choice right).
One hunting **plumbing** (does it reach the consumer, is it wired, does anything downstream undo it).
These find different classes. In practice the mechanism review has passed work the plumbing review
then killed.

### 6. Verify the defect exists in THAT source before repairing it
The ninth failure, and the first that was not a wrong-object check. A contamination was diagnosed **by
analogy**: a sibling feed was genuinely corrupted, the same signature appeared here, so the same cause
was assumed. The signature was real; the cause was not operating. The source data for this feed turned
out to be already corrected, and 91% of the "repair" damaged good data.

A shared symptom is not a shared cause. Trace the suspected defect to the specific file the feature is
built from, and test THAT file for the property you are assuming. Eight sealed rules cannot catch a
false premise they were written on top of — every instrument built afterwards will confirm it, because
they all measure the symptom and none of them measure the cause.

Corollary: when a repair is large, ask what single fact, if false, would make the whole thing
unnecessary. Then go and measure that fact first.

### 7. The claim you make right after a big retraction is the least-scrutinised in the room
The tenth failure. A session wrote Rule 6 — "verify the defect exists in THAT source, a shared symptom
is not a shared cause" — and then, **one section later in the same document**, diagnosed a second
contamination from a symptom threshold alone without testing that name's source. It was wrong; the
name's prices were fully adjusted and the extreme reading was a real crash.

A rule written from a failure does not immunise the session that wrote it. After a retraction there is
pressure to re-establish footing, and the next claim gets made with the least evidence and the most
confidence. Slow down precisely there.

Related, same session: a correction issued in conversation but never written into the document on
disk. **The record is what executes, not the conversation.** If a claim is retracted, amend the file —
a stale prescription in a document will be followed by whoever reads it next, including you tomorrow.

## Supporting disciplines

- **Pre-register and seal.** Write the rules from mechanism, hash them, and have the runner verify the
  hash and void itself if the document changed. Deriving rules after seeing output is not a check.
- **Back up before changing.** Whole-directory archive plus the specific live files a promotion would
  overwrite. Then *open the archive* — an untested backup is not a backup.
- **Never write to live.** Build candidates, diff, promote as a separate, deliberate act.
- **Show the whole ledger, not the latest item.** Findings reported one at a time read as chaos and
  feel like things are being lost. Keep a numbered open-items list and show it.
- **Verify documentation.** "The doc says it is adjusted" is unverified by default. In this programme,
  four documents asserted something was corrected or applied when it was not.
- **Do not over-declare damage either.** Prove what is affected before discarding sound work.

## The closing move

Every defect found becomes a permanent assertion in the regression suite, in the same session it is
found. Prose cannot stop a defect returning. If it is not an assertion, it will come back.
