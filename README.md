# Scientific Writing Skills

**A Claude plugin for scientific writing** — six AI skills that edit research prose, structure IMRaD manuscripts, run the writing process, handle peer review and publication ethics, draft grant proposals, and translate research for general audiences.

Distilled from all eight units of Stanford's [*Writing in the Sciences*](https://online.stanford.edu/courses/som-y0010-writing-sciences) (Kristin Sainani) — 62 lecture transcripts, ~141,000 words — into instructions an AI assistant can actually act on, plus four Python scripts that catch mechanically what a reviewer would catch by eye.

Works with [Claude Code](https://claude.com/claude-code), Claude Cowork, and any tool that supports the Claude Agent Skills format.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## What it looks like

A paragraph from `examples/`, before and after `sciwrite-prose`:

**Before**

> As it is well known, the implementation of a hardware acceleration strategy provides a reduction in the inference latency of convolutional neural networks that are deployed on resource-constrained embedded platforms. However, a degradation of the detection accuracy is caused by the quantisation of the network weights to eight-bit integers. Therefore, there is a significant increase in memory pressure when the batch size is raised above four. Furthermore, the results were not inconsistent with those reported for comparable architectures, and the overhead was not significant. Moreover, the proposed pipeline for real-time defect detection, which combines a lightweight backbone with a hardware-accelerated non-maximum suppression stage running on the programmable logic of the Kria KV260, achieves 31 frames per second at 1080p. The DPU IP was integrated into the PL via AXI4, and the PS ran a PetaLinux image with the XRT stack managing DMA transfers between DDR and BRAM. Due to the fact that a majority of the successful solutions rely on this approach, we adopted it.

**After**

> Hardware acceleration cuts inference latency for convolutional neural networks on resource-constrained embedded platforms, but quantising the weights to eight-bit integers costs detection accuracy, and memory pressure climbs sharply once the batch size passes four.
>
> Our pipeline pairs a lightweight backbone with hardware-accelerated non-maximum suppression on the programmable logic of the Kria KV260, reaching 31 frames per second at 1080p. The deep-learning processing unit talks to the programmable logic over AXI4, and the processing system runs a PetaLinux image whose runtime moves data between DDR and block RAM. These results match those reported for comparable architectures, and the overhead stays under 3%. We chose this design because most published solutions rely on it.

| | Before | After |
|---|---|---|
| Words | 165 | **112** |
| Sentences | 7 | 5 |
| `to be` verbs per 100 words | 4.8 | **0.0** |
| Nominalisations per 100 words | 6.7 | 4.5 |
| Defects flagged by `prose_audit.py` | 25 | **4** |

Same claims, same numbers, a third shorter. The skill named every one of those 25
defects and said why; the script found them without reading for meaning.

---

## What it does

You paste a paragraph and ask why it feels bloated. It tells you: a smothered verb, a throat-clearing opener, a nominalisation, and a buried predicate — and hands you the rewrite.

You ask where to start on a paper. It tells you the tables and figures come first, and why.

You get a decision letter that looks like a rejection. It tells you that "revise and resubmit" is the outcome you were aiming for, and drafts the point-by-point response.

```
you   → "review the discussion section of my thesis chapter"
claude → reads the .tex, extracts that section, runs the audits,
         reports what to fix in order of impact
```

---

## The six skills

| Skill | Use it for | Course units |
|---|---|---|
| **sciwrite-prose** | Sentence and paragraph editing: clutter, active voice, verbs, nominalisations, punctuation, parallelism, keyword consistency, acronyms | 1–3 |
| **sciwrite-manuscript** | IMRaD structure: tables and figures, Results, Methods, Introduction, Discussion, Abstract; verb tense per section | 5 |
| **sciwrite-process** | Getting it written: pre-writing, the 70/10/20 split, drafting without perfectionism, revision, pre-submission checklist | 4 |
| **sciwrite-publish** | Journal choice, submission, responding to reviewers, doing a peer review, authorship, plagiarism, predatory journals | 6 |
| **sciwrite-proposals** | Review articles, grant specific aims and research plans, recommendation letters, personal statements | 7 |
| **sciwrite-outreach** | Lay summaries, press interviews, risk communication, science news stories, social media | 8 |

Each skill keeps its `SKILL.md` short and loads detailed reference files only when the task needs them, so asking for a one-paragraph cleanup does not drag eight units of doctrine into context.

---

## The scripts

Four Python scripts (standard library only, no dependencies) do the mechanical detection so the model spends its attention on judgment:

| Script | What it finds |
|---|---|
| `extract_text.py` | Plain text and a section map from `.tex`, `.docx`, `.md`, `.txt` — so "review my Discussion" works on a real LaTeX manuscript without pasting anything |
| `prose_audit.py` | Dead-weight phrases, blobs, long-for-short, redundancy, passive voice, `to be` density, nominalisations, buried predicates, double negatives, `there is/are`, adverbs, undefined acronyms, transition-word pile-ups, paragraph length |
| `keyword_consistency.py` | Terminology drift between sections (Methods says *obese group*, Results says *heavier group*), and acronyms defined in one section but reused in another |
| `numeric_consistency.py` | Sample sizes that disagree across sections, abstract numbers absent from the body, excessive significant figures, mismatched precision in `mean ± SD` |

Everything supports `--json`. They report **candidates, not verdicts** — passive voice is legitimate in Methods, a repeated keyword is mandatory, and `PSNR` may be standard in your venue.

```bash
python scripts/prose_audit.py paper.tex --section discussion
python scripts/keyword_consistency.py paper.tex --terms "obese group,control arm"
python scripts/numeric_consistency.py paper.tex --json
```

---

## Install

### Claude Code

```bash
git clone https://github.com/dvdsosa/scientific-writing-skills.git
claude plugin install ./scientific-writing-skills
```

Or add the marketplace and install from it:

```bash
claude plugin marketplace add dvdsosa/scientific-writing-skills
claude plugin install sciwrite
```

### Running the scripts

The skills call the scripts through `$SCIWRITE`, which resolves either way:

```bash
SCIWRITE="${CLAUDE_PLUGIN_ROOT:-$(cd -P ~/.claude/skills/sciwrite-prose/../.. && pwd)}"
python "$SCIWRITE/scripts/prose_audit.py" paper.tex
```

`CLAUDE_PLUGIN_ROOT` is set only for a plugin install. If you symlinked or copied
the skills into `~/.claude/skills/` instead, the fallback resolves the repository
from the skill directory, so the same command works in both cases. To call the
scripts directly from anywhere, point at the clone:

```bash
python ~/path/to/scientific-writing-skills/scripts/prose_audit.py paper.tex
```

Pass the **master** `.tex` file, not a single chapter: `keyword_consistency.py`
and `numeric_consistency.py` compare *across* sections, and an isolated fragment
gives them nothing to cross-check.

### As individual skills

Copy any `skills/sciwrite-*/` directory into `~/.claude/skills/`. Each skill is
self-contained apart from the shared `scripts/`; if you install skills
individually, copy `scripts/` alongside them and adjust the paths in the
`SKILL.md` files.

### Verify

```bash
python scripts/prose_audit.py --help
```

Python 3.8+. No third-party packages.

---

## Design notes

**Traceability.** Every rule cites the course module it comes from, so you can
check any of them against the source. Conventions of your own — your supervisor's,
your group's, your target journal's — are stated in the conversation, and the
skills follow them and tell you which course rule they override.

**The em dash stays.** Some scientific-writing prompts ban it as a marker of
machine-generated text. This plugin does not, because the course teaches the dash
as the most versatile mark available and demonstrates case by case where commas
lose the emphasis and parentheses bury essential information. The real constraint
— use it sparingly, reserve it for the hard jobs — is already in the source.

**Two example registers.** The course's own examples are biomedical and are
quoted as such. A second set in
`skills/sciwrite-prose/references/engineering-examples.md` applies the same rules
to embedded systems, FPGA design and computer vision, clearly marked as written
for this plugin rather than drawn from the course.

**Language.** The skills are written in English; they answer in whatever language
you write to them in.

---

## What this is not

- **Not a substitute for reading the course.** It is free, it is excellent, and
  eleven hours of Kristin Sainani will teach you things a plugin cannot.
- **Not a content reviewer.** It improves how claims are delivered, never the
  claims themselves. If something looks scientifically wrong it flags it and
  leaves it alone.
- **Not a plagiarism checker.** For overlap against your own bibliography, see
  tools built for that.
- **Not affiliated with Stanford University or Kristin Sainani.** This is an
  independent, non-commercial study aid built from publicly available course
  materials. All pedagogical credit belongs to the course; any errors in
  transcription or interpretation are mine.

---

## Contributing

Corrections against the source material are especially welcome — if a rule here
misrepresents what the course teaches, that is a bug. See [CONTRIBUTING.md](CONTRIBUTING.md).

Good first contributions: additional worked before/after pairs from your own
field; false positives in the audit scripts; translations of the reference files.

---

## Credits

Course: **Writing in the Sciences**, Kristin Sainani, Stanford University.

Books the course recommends, and which stand behind much of this material:
William Zinsser, *On Writing Well*; Strunk & White, *The Elements of Style*;
Mimi Zeiger, *Essentials of Writing Biomedical Research Papers*; Thomas Annesley's
series in *Clinical Chemistry*.

Grant-writing material in `sciwrite-proposals` derives from guest lectures by
Crystal Botham and Sky Brubaker (Stanford Biosciences Grant Writing Academy);
science-communication material in `sciwrite-outreach` from guest lectures by Amy
Adams (Stanford Science Communication).

## License

[MIT](LICENSE) for the plugin code and the written instructions. The underlying
course is © Stanford University; this repository quotes short excerpts for
educational commentary and does not redistribute course materials.

---

<sub>Keywords: scientific writing · academic writing · manuscript editing · research paper writing · IMRaD · peer review · grant writing · specific aims · lay summary · science communication · Claude skills · Claude Code plugin · AI writing assistant for researchers · thesis writing · journal submission</sub>
