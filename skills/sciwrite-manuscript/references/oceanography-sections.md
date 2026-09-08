# Section-level patterns in physical oceanography

The course teaches IMRaD with biomedical examples: a trial, a cohort, a dose.
Observational oceanography keeps the same skeleton but fills it differently —
the "subjects" are cruises and sections, the "intervention" is usually nothing,
and the reader's first question is *how confident are you in that number?*

**Provenance:** the structural rules come from the course. The example text
below was written for this file to show the pattern; no sentence is taken or
adapted from a published paper.

---

## What changes, section by section

| Section | Biomedical default | Oceanographic equivalent |
|---|---|---|
| Methods opens with | study design, population | the cruises: dates, ship, section line, station spacing |
| The "sample" is | patients enrolled | stations occupied, and the years they were occupied |
| Randomisation and blinding | central to validity | absent — validity rests on the inverse model's constraints |
| The headline number | effect size with CI | transport in Sv with its uncertainty |
| The rival explanation | confounding | aliasing of a seasonal or eddy signal by a one-off snapshot |

Everything else — one idea per paragraph, the upshot first, keywords identical
across sections — is unchanged.

---

## 1. Methods: the cruise paragraph

Reviewers check reproducibility here first. The order that works:

1. **The section.** Where it runs, which line designation (A05, P06), station
   spacing, and where spacing was tightened.
2. **The cruises.** Dates, ship, and which occupation is new versus reanalysed.
3. **The instruments.** CTD, lowered and shipboard ADCP, with calibration and
   accuracy figures.
4. **The model.** Layer definitions, the constraints imposed, and — critically —
   what the reference level is and why.
5. **The uncertainty.** How the error bars were produced.

The reference level deserves its own sentence. It is the single assumption a
sceptical reader will attack, and burying it inside a list invites the attack.

> **Thin.** An inverse box model was applied to the hydrographic data.
>
> **Reproducible.** We applied an inverse box model with eleven neutral-density
> layers, conserving mass overall and within each layer, and referenced the
> initial geostrophic velocities to the deepest common level. Layer boundaries
> follow [ref, Table 1].

---

## 2. Results: transports, not tables read aloud

The commonest defect in this literature is a Results section that walks the
reader down a column of numbers already printed beside it.

**Report:** the pattern, its magnitude, whether it exceeds the uncertainty, and
where it sits relative to earlier occupations.

**Do not report:** every value in the table; the fact that a table exists; the
same number in text, table and abstract in three different precisions.

> **Recital.** The upper-layer transport was 16.3 ± 1.2 Sv in 2003 and
> 17.1 ± 1.4 Sv in 2011 (Table 3).
>
> **Result.** Upper-layer transport increased by 0.8 Sv between occupations, well
> within the combined uncertainty of the two estimates (Table 3).

Significant figures travel with the uncertainty. `16.34 ± 1.2 Sv` claims a
precision the error bar denies; write `16.3 ± 1.2`. The number in the abstract
must be the number in the table.

---

## 3. Discussion: open with the answer, not the caveats

A discussion that opens with limitations tells the reader the authors do not
believe their own result. Limitations belong after the interpretation, and each
one should be paired with what it does and does not affect.

The field-specific limitation that must appear: **a hydrographic section is a
snapshot.** If the analysis rests on two occupations a decade apart, say plainly
that interannual and eddy variability cannot be separated from any trend. A
reviewer will raise it; raising it first is cheaper.

> **Weak.** Our results should be interpreted with caution because of the limited
> number of cruises.
>
> **Specific.** Two occupations a decade apart cannot separate a trend from
> interannual variability. The 0.8 Sv change we report is therefore an upper
> bound on any secular signal, not evidence of one.

---

## 4. Introduction: narrow to the gap, do not survey

The pull towards a general review of the overturning circulation is strong and
should be resisted. The funnel:

1. Why this circulation matters — two or three sentences, not two paragraphs.
2. What repeat sections have established at this latitude.
3. **The gap**: which years are missing, which layer is unconstrained, which
   disagreement between estimates is unresolved.
4. What this paper does about it.

If the introduction could preface any paper about the same basin, it is a review,
not an introduction.

---

## 5. Abstract: the numbers a reader will quote

For a transport paper the abstract has to carry the headline transports with
their uncertainties, the years compared, and the one claim the paper defends.
Readers cite abstracts; make the citable numbers correct and identical to the
table.

Checklist before submission:

- [ ] Every number in the abstract appears in the body with the same precision.
- [ ] Layer names match the Methods definitions exactly.
- [ ] The section line and the years are both stated.
- [ ] Any acronym in the abstract is expanded there, not only in the body.

---

## 6. Tables and figures

- A **station map** is not optional. Geometry described in prose is geometry the
  reader reconstructs wrongly.
- A **transport table** is read across occupations, so occupations belong in
  columns and layers in rows.
- **Uncertainties belong in the table**, not only in the text. A transport
  without its error bar is not a result.
- Colour scales for velocity sections must be **diverging and centred on zero**,
  or the reader misreads the sign of the flow.
