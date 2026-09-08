# Worked examples, section by section

Course examples are marked with their module. Engineering examples were written
for this plugin to exercise the same patterns in a different register — the rules
are the course's, the sentences are not.

---

## Introduction: the known / unknown / aim skeleton

### Course example — academic spam (module 5.5)

Two paragraphs. The whole introduction.

> **[known]** *Unsolicited and unwanted (spam) electronic invitations to speak at
> or attend conferences or to write for or edit journals are a burgeoning aspect
> of academic life. Colleagues regard such invitations with wry amusement,
> intense frustration or resignation. Two of us have reviewed travel grant
> applications from colleagues who received spam invitations to give conference
> presentations.*
>
> **[unknown]** *Few studies have focused on academic spam.*
>
> **[this study]** *We investigated the amount, relevance, content, and
> suppressibility of academic emails.*

The unknown is one sentence. The aim names four things — and those four are
exactly what the discussion answers, in order. That correspondence is the point.

### Course example — obesity and cancer mortality (module 5.5)

Alternates known and unknown, which is common:

- known: excess weight raises all-cause and cardiovascular mortality; it matters
  in cancer generally
- unknown: the magnitude, and which individual cancers
- known: consistent associations for endometrium, kidney, gall bladder, breast
  (post-menopausal), colon in men
- unknown: pancreas, prostate, liver, cervix, ovary and blood cancers are scarce
  or inconsistent — *summarised in a single sentence, with no study-by-study walk*
- why the question is open: few prospective studies, inconsistent categorisation
  of overweight, smoking bias
- this study: *We conducted a prospective investigation in a large cohort of U.S.
  men and women to determine the relations between body mass index and the risk
  of death from cancer at specific sites.*

Every gap named in the "unknown" is answered by a design feature named in the
last sentence: prospective, large, BMI rather than arbitrary categories.

### Engineering version

> **[known]** *Convolutional detectors now run in real time on embedded
> accelerators, and several vendors ship toolchains that quantise and deploy them
> automatically [refs].*
>
> **[unknown]** *How much accuracy that automated quantisation costs is reported
> inconsistently: published figures range from under one point to more than eight,
> across benchmarks that differ in resolution, class balance and backbone.*
>
> **[gap in prior work]** *No study has held the deployment target fixed while
> varying the backbone, so the reported spread cannot be attributed to the
> quantisation itself.*
>
> **[this study]** *We measured post-quantisation accuracy and latency for three
> backbones on a single Kria KV260 target, using one dataset and one toolchain
> version, to isolate the cost of automated quantisation.*

Note the shape: the gap is not "nobody has done this", it is "the existing
numbers cannot answer the question because of how they were produced" — which is
what makes the study necessary rather than merely new.

---

## Results: summary versus recitation

### Course example — the witches table (module 5.2)

**As written by a student:**

> *The characteristics of the bad witches and the good witches are shown in Table
> 1. The mean age of the bad witches was 45 ± 5, and the mean age of the good
> witches was 36 ± 6. Gender was similar between the groups with 85 % female in
> the bad witches and 83 % female in the good witches. The mean BMI of the bad
> witches was…*

**Edited:**

> *The witches were on average lean and predominantly female (Table 1). Bad
> witches were significantly older, had higher blood pressure, exercised less,
> and were more likely to smoke than good witches. More bad witches were
> unemployed, but this difference did not reach statistical significance.*

No numbers at all, and nothing is lost — the table has them. The first sentence
of the original, announcing what Table 1 contains, is deleted entirely.

### Course example — running during pregnancy (module 5.3)

Here some numbers *do* belong, because this table carries the study's main
result. The edit keeps four and drops a dozen:

> *70 % of runners ran during pregnancy (n = 77), and almost one-third ran during
> the third trimester. On average, those who ran during pregnancy greatly
> curtailed their training — running just 20.3 ± 9.3 miles per week and cutting
> their intensity to about half of their non-pregnant running effort. Three
> reported sustaining a running injury while pregnant. In the postpartum period,
> nearly a quarter waited two or fewer weeks to resume running, and most resumed
> within two months.*

Two things to notice. *47.9 ± 21 %* became *about half*, because the precision
was not the point. And *3.9 %, 3 out of 77* became *three*, because three is
self-evidently a small number.

### Engineering version

**Recitation:**

> *Table 3 shows the results for the three configurations. The mean latency of
> configuration A was 12.4 ± 1.3 ms, the mean latency of configuration B was 9.8
> ± 1.1 ms, and the mean latency of configuration C was 9.6 ± 1.4 ms. The
> accuracy of configuration A was 91.2 %, of configuration B 93.7 %, and of
> configuration C 93.9 %.*

**Summary:**

> *Hardware acceleration cut mean latency by roughly a quarter with no loss of
> accuracy, and the two accelerated configurations were indistinguishable from
> each other (Table 3). The accuracy gap that matters is between the baseline and
> either accelerated variant: 2.5 points.*

The one number promoted into the text is the one the study exists to estimate.

---

## Discussion: answering the question you asked

### Course example — low-carb versus low-fat (module 5.7)

The introduction ended with two questions: (a) greater weight loss on a
carb-restricted diet, and (b) without harming heart health.

Paragraph 1, first sentence, answers (a):

> *We found that severely obese subjects with a high prevalence of diabetes and
> pre-diabetes lost more weight in a six-month period on a carb-restricted diet
> than on a fat- and calorie-restricted diet.*

Paragraph 2 answers (b). Paragraph 4 gives the limitations — and gives them well:
many participants were on lipid-lowering and antihypertensive drugs, which could
plausibly drive the cardiovascular findings, so the authors re-ran the analysis
excluding those participants and reported that the result held. Paragraph 6 adds
the high attrition rate.

Paragraph 7 restates both answers, then adds the caution that keeps the paper
honest:

> *This study proves a principle and does not provide clinical guidance. Given
> the known benefits of fat restriction, future studies evaluating long-term
> cardiovascular outcomes are needed before a carb-restricted diet can be
> endorsed.*

That last move — refusing to overstate — is what a careful reviewer is looking
for.

### How not to open a discussion (module 5.7)

> *This meta-analysis is subject to a number of limitations.*

Start with what you found. The limitations go several paragraphs down.

### Engineering version, opening paragraph

> *We found that automated eight-bit quantisation costs between 1.1 and 2.4
> accuracy points on the KV260, and that the spread across backbones is far
> narrower than the published range suggests. The depthwise-separable backbone
> lost the most, which we did not anticipate.*

*We found that*, then the answer, then an explicit note that one finding was
novel or unexpected. Saying which results surprised you is not a weakness; it is
the sentence a reader remembers.

---

## Abstract: pulling from the finished paper

### Course example — academic spam (module 5.8), structured

- **Background / objectives** — *to assess the amount, relevance, content and
  suppressibility of academic spam invitations to attend conferences or submit
  manuscripts*
- **Design, setting, participants** — five academics
- **Main outcome measures**
- **Results** — *at baseline, recipients received an average of 312 spam
  invitations each month. Unsubscribing reduced the frequency by 39 % after one
  month, but by only 19 % after one year. Overall, 16 % of spam invitations were
  duplicates and 83 % had little or no relevance to the recipients. Spam
  invitations were characterised by inventive language, flattery and exuberance.*
- **Conclusion** — *academic spam is common, repetitive, often irrelevant and
  difficult to avoid or prevent.*

The results answer the four objectives in the order they were stated. That
alignment is what makes an abstract feel tight.

### The missing sentence most abstracts have

The implication. One sentence at the end saying why this matters beyond the
study. It is the first thing a journalist or an outside reader looks for, and the
easiest thing to leave out because you are already at the word limit.

---

## A whole-manuscript failure mode: numbers that disagree

From module 4.6, and worth keeping in mind because it costs nothing to prevent
and is expensive to be caught on:

- Methods: *we followed participants for a minimum of two years.*
- Results: *the average follow-up time was one and a half years.*

Both cannot be true. Whatever the author meant, a reviewer now doubts the whole
analysis. Same for an abstract that reports different numbers from the body, and
for a table and a figure that should match and do not:

> If you can't keep track of your dataset, that makes me worry about the whole
> analysis. — module 4.6

Run `numeric_consistency.py` before submitting.
