# Final-draft checklist

Source: module 4.6.

Run this when the prose is done and before the manuscript goes to a journal, a
supervisor or a thesis committee. None of it is about writing quality. All of it
is about the things that make a reviewer stop trusting the paper.

---

## 1. Internal consistency

Read the manuscript looking only for statements that contradict each other in
different sections.

> Methods: *We followed participants for a minimum of two years.*
> Results: *The average follow-up time was one and a half years.*

The average cannot be below the minimum. Perhaps they meant a maximum of two
years, or that they aimed for two. Whatever the intent, a reviewer who spots this
does not think "typo" — they think the authors are not in control of their own
study.

Check specifically:

- [ ] Inclusion and exclusion criteria stated the same way everywhere
- [ ] Follow-up periods, durations and timepoints consistent
- [ ] Group definitions identical in Methods, Results, tables and figures
- [ ] Number of experiments, runs, replicates or sites consistent
- [ ] Anything described as "minimum", "maximum" or "average" arithmetically
      compatible with everything else

---

## 2. Numerical consistency

The most common source of red flags, and the easiest to prevent.

- [ ] Every number in the abstract appears, and matches, in the body
- [ ] Sample sizes agree: abstract, Methods, Results, tables, figure legends
- [ ] Percentages match the raw counts they came from
- [ ] Table values match the figures that plot them
- [ ] Significant figures consistent, and justified by the measurement precision
- [ ] Means and their spreads carry the same precision (`12.4 ± 1.3`, not
      `12.4 ± 1.32`)
- [ ] Units present on every quantity, in tables especially

Where mismatches come from: sloppy copy-paste, or re-running an analysis and
updating only part of the manuscript. Both are innocent. Neither looks innocent.

> I was reviewing one paper where the numbers in a table and figure should have
> been identical, but they didn't match. So I suspected that the authors had more
> than one version of their dataset running around. If you can't keep track of
> your dataset, that makes me worry about the whole analysis. — module 4.6

```bash
# Plugin install: CLAUDE_PLUGIN_ROOT is set for you.
# Skills-only install (symlinked or copied into ~/.claude/skills/): resolve it.
SCIWRITE="${CLAUDE_PLUGIN_ROOT:-$(cd -P ~/.claude/skills/sciwrite-prose/../.. && pwd)}"

python "$SCIWRITE/scripts/numeric_consistency.py" paper.tex
```

---

## 3. References that go somewhere

A **reference to nowhere** is a citation whose target does not contain the
information attributed to it. These are not rare — checking references
systematically, the majority turn out not to contain the promised information.

The failure modes:

- The source says something related but does not support the specific statement.
- The citing author exaggerated or reinterpreted the finding.
- The citing author was selective about which part of the source they mentioned.
- The reference is simply numbered wrong, or placed at the wrong sentence.
- The URL is dead.

A worked case from the course: an author wrote *the UVC emission is even larger
than ambient sunlight on a mountain*, citing two sources. The first was a broken
link with no relevant content anywhere on the site. The second, a full paper, did
not contain the words *ambient sunlight*, *mountain* or *UVC*.

- [ ] Every reference checked against the sentence it supports
- [ ] Reference numbering verified after the last round of edits (a reference
      manager prevents most of this)
- [ ] URLs still live

---

## 4. Primary sources

Do not inherit citations from other papers' reference lists. Statistics degrade
as they propagate — the game of telephone, in the literature.

The course's case study: a prevalence figure of "15 to 62 %" appeared in every
paper in a subfield through the 1990s and 2000s, with roughly fifty different
attributions. Tracing it back, it came from three studies published in the 1980s:
cross-sectional self-report surveys, no control groups, convenience samples, one
of them 42 gymnasts and another a group of 9-to-18-year-olds at a swim camp — who
were routinely described downstream as "college athletes". The number was cited
as a gold standard for two decades and could not support the weight.

- [ ] Every key statistic traced to its original study, not to a review
- [ ] The original study's design actually supports the claim being made
- [ ] Where a summary of the literature is borrowed rather than done afresh, it
      is quoted and attributed (see `sciwrite-publish/references/plagiarism.md`)

Scientific journals rarely have fact-checking departments. Nobody downstream will
catch this for you.

---

## 5. Formatting for the target journal

- [ ] Author instructions read in full, and followed
- [ ] Reference style matches the journal's
- [ ] Table and figure formatting copied from a published paper in that journal
- [ ] Word, figure and reference limits respected
- [ ] Ethics approval statement present, if applicable
- [ ] Funding sources and conflicts of interest declared
- [ ] Acronyms defined in every section, including tables and legends

---

## 6. Last prose pass

- [ ] Read the whole thing out loud, or have it read to you
- [ ] Verb check on the introduction and discussion
- [ ] Someone outside your niche has read it and can tell you back the main
      finding, the take-home message, and why it matters

```bash
# Plugin install: CLAUDE_PLUGIN_ROOT is set for you.
# Skills-only install (symlinked or copied into ~/.claude/skills/): resolve it.
SCIWRITE="${CLAUDE_PLUGIN_ROOT:-$(cd -P ~/.claude/skills/sciwrite-prose/../.. && pwd)}"

python "$SCIWRITE/scripts/prose_audit.py" paper.tex
python "$SCIWRITE/scripts/keyword_consistency.py" paper.tex
```
