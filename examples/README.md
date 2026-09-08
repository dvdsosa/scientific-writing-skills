# Examples

Fixture files with deliberately planted defects, used to check the scripts and to
show what the skills catch. Every defect below is one the course names.

## Files

| File | Planted defects |
|---|---|
| `cluttered-paragraph-edited.md` | none — the same paragraph after `sciwrite-prose`. 165 → 112 words, 25 flagged defects → 4. Run the audit on both to compare |
| `cluttered-paragraph.md` | throat-clearing opener, blob, long-for-short, redundant adjective, smothered verb, two passives, buried predicate, double negative, `there is`, intensifier, five undefined acronyms, four transition-word openers |
| `manuscript.tex` | keyword drift (*obese/heavier*, *lean/lighter*), acronym defined only in Methods, four significant figures on a frame rate, mismatched precision in `mean ± SD`, an abstract number absent from the body, Results reciting the table, Discussion opening with limitations, Introduction as a general literature review |

## Try it

```bash
python ../scripts/prose_audit.py cluttered-paragraph.md
python ../scripts/extract_text.py manuscript.tex
python ../scripts/keyword_consistency.py manuscript.tex
python ../scripts/numeric_consistency.py manuscript.tex
```

## What a correct run finds

`prose_audit.py` on `cluttered-paragraph.md` should report, at minimum:

- **clutter** — `as it is well known`, `due to the fact that`, `a majority of`,
  `successful solutions`
- **verbs** — `provides a reduction in` (smothered), `is caused by` (passive),
  `was integrated` (passive), a buried predicate before *achieves*
- **negatives** — `not inconsistent`, `not significant`
- **expletives** — `there is`
- **adverbs** — `significant`, used non-statistically
- **acronyms** — `DPU`, `PL`, `PS`, `XRT`, `BRAM` undefined at first use
- **paragraphs** — four sentences opening with a transition word

`keyword_consistency.py` on `manuscript.tex` should report the two synonym pairs
(*obese group* / *heavier group*, *lean group* / *lighter group*) and flag `DPU`
as defined only in Methods.

`numeric_consistency.py` should report `31.4573` as over-precise, `12.4 ± 1.03`
as mismatched precision, and the sample size `930` appearing in abstract and
Methods.

If a run misses one of these, that is a regression. If it flags something not on
this list, check whether it is a false positive worth narrowing — see
[CONTRIBUTING.md](../CONTRIBUTING.md).
