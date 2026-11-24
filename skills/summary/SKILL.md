---
name: summary
description: Produce a structured, scannable status-and-next-steps brief — fixed headings in a fixed order (what's settled, the ONE decision needed, each workstream, commands only the user can run, decisions coming later, ETA), plain English, every claim tagged verified / reported / assumed. Use when the user asks for a summary, a brief, a status, "where do we stand", "what are the next steps", "explain this to me", a handover, or invokes /summary. Also use unprompted after a long investigation, after multiple agents report, or before the user must make a call.
---

# Summary: the structured brief

The reader is one person running many threads. They have been away, and they will act on this and
nothing else. Assume they remember **nothing**: not the jargon, the file names, or last week's
conclusion. Fixed headings make a long conversation easy to re-enter.

## The shape: fixed headings, always in this order

Leave out a section that has nothing in it. Never reorder the ones you keep.

```
# <Project>: <what this is> (<Day DD Mon>, <HH:MM> <timezone>)   ← read the clock: run `date`

## 1. What I've recorded / what's settled
- The user's decisions from their last message, one line each, in their terms. A new decision
  replaces an old one: say what it replaced in a few words, without friction.
- Anything they wrote that got cut off or is ambiguous: say so here and give your reading.

## 2. The one thing I need from you
- Exactly ONE decision, the highest-leverage one. Give it a table if there are 3+ comparable parts.
- My recommendation, the one fact that decides it, and what I rejected and why.
- End with the question in bold: **Your call: …?**

## 3. The streams (one H3 per workstream / owner)
### <Stream name> (<owner>), <status: briefed / running / done>
**Done:** what landed, with its tag.
**Next:** numbered steps, in order. Mark the ones that need the user.

## 4. Commands only you can run
- One bullet per command, with what it does. A command that's ready goes in a code block at the
  END of the message (see "Commands" below).

## 5. Decisions coming later, one at a time
1. Numbered, in the order they'll be asked, each with my default in brackets.

## 6. Other findings (only if any)
- Retractions, cross-project findings, risks. Each finding gets its own line and verdict, even when
  two share a subject.

**ETA:** when the next results land, with the timezone.
```

## Rules for every section

- **Headings carry the structure; bullets carry the content.** No paragraph longer than three lines.
  Use a table whenever three or more things are compared.
- **Lead with the answer** in every bullet. Never build up to it.
- **Plain English.** Expand a term the first time it appears. Attach the meaning to every number
  ("$30 worst case per customer, once", not just "$30").
- **Tag claims when it matters:** ✔ verified by me (name the file, number or check) · ◐ reported by
  someone else, unverified · ? assumed. A claim with no tag reads as verified.
- **Exactly one decision in section 2.** Everything else that needs the user waits in section 5. A
  queue of asks is the failure this format exists to prevent.
- **Retractions go in section 6, at full weight.** Say what you said, what's true, and what it
  changes, in one or two sentences. No apology, no footnote.
- **Report checked-and-clean results.** "Looked, found nothing" only counts with the control that
  could have failed.
- **Synthesise agent reports.** Never relay them. Say when two independent routes reached the same
  finding.
- **Two findings that share a subject are two findings.** Give each its own verdict. A tidy summary
  invites collapsing them, and that is how a live blocker becomes "false alarm".

## Commands

If the user asked for a command, or a command is ready for their hands, the message ENDS with it, in
a code block, ready to paste, with the rollback line under it:

```
! bash ~/path/to/push.sh
# rollback: ! bash ~/path/to/rollback.sh
```

## Never

- Never bury the decision below the streams.
- Never ask for more than one decision.
- Never an untagged number that something gets acted on.
- Never end without the ETA (and the command, when one was asked for).
- Never "we did a lot of work". Say what it means.
