# Worked edits in physical oceanography

The course's own examples are biomedical. These apply the same rules to
hydrography, ocean circulation and transport estimation, so the patterns are
recognisable in that register.

**Provenance:** the *rules* come from the course; these *sentences* do not. They
were written to exercise the same defects in the vocabulary of the field —
inverse box models, GO-SHIP sections, water masses, transports in sverdrups.
No sentence here is taken or adapted from any published paper. Cite the course
for the principle, not for these examples.

---

## 1. Throat-clearing, nominalisation and a smothered verb

> **Before.** As is well known, the application of an inverse box model
> methodology provides an improvement in the estimation of the absolute
> geostrophic transports that are derived from repeat hydrographic sections.

Diagnosis: *As is well known* is the author clearing their throat — a citation
says it with no words. *The application of* and *the estimation of* are
nominalisations. *Provides an improvement in* is a smothered verb (*improves*).
*Methodology* is *method*. The main verb waits thirteen words.

> **After.** Inverse box models improve absolute geostrophic transports
> estimated from repeat hydrographic sections [ref].

22 words to 12. The citation carries what the opener was claiming.

---

## 2. Passive voice hiding who did the work

> **Before.** The station data were quality-controlled and the outliers were
> removed before the model was run.

Three passives in fourteen words, and the reader cannot tell whether the authors
did this or inherited it already done from the data centre. That distinction
matters for reproducibility.

> **After.** We quality-controlled the station data and removed outliers before
> running the model.

Methods is the one section where passive is often right — it keeps the focus on
the procedure. But use it *because you chose to*, not by default. Here the actor
is the point.

---

## 3. Cause and effect inverted by the passive

> **Before.** A reduction in the northward heat transport is caused by the
> weakening of the upper limb of the overturning circulation.

The sentence puts the effect first and the cause last, so the reader assembles
the logic backwards.

> **After.** A weaker upper limb of the overturning circulation reduces northward
> heat transport.

Cause, verb, effect. Seventeen words to twelve, and the agent is visible.

---

## 4. Buried predicate

> **Before.** The transport of North Atlantic Deep Water across the section,
> computed from the velocities of the inverse model after the imposition of mass
> conservation constraints within each layer, decreased between the two
> occupations.

Subject and verb sit twenty-eight words apart. The reader holds *the transport*
in memory through an entire clause before learning what it did.

> **After.** North Atlantic Deep Water transport across the section decreased
> between the two occupations. The velocities come from the inverse model, which
> conserves mass within each layer.

Split it. The main claim lands in the first sentence; the method follows.

---

## 5. *There is*, and the verb hiding underneath

> **Before.** There is a significant difference in the abyssal transports between
> the two cruises.

*There is* postpones the verb and *difference* is the action in noun form. And
*significant* here is doing double duty — statistical or merely large?

> **After.** Abyssal transports differ between the two cruises (p < 0.05).

Or, if the difference is not statistical: *Abyssal transports are markedly larger
in 2011*. Say which you mean.

---

## 6. Keyword drift across sections

> **Methods.** …transports of Antarctic Intermediate Water (AAIW)…
> **Results.** …the intermediate layer carried 4.2 ± 0.8 Sv northward…
> **Discussion.** …this mid-depth water mass…

Three names for one thing. A reader who does not already know the field asks
whether *the intermediate layer* is the same object as AAIW, or a depth range
that happens to contain it. Synonyms are a virtue in an essay and a defect here.

> **After.** *Antarctic Intermediate Water (AAIW)* at first use, then *AAIW*
> everywhere — Methods, Results, Discussion, table headings, figure legends.

Pick the term once and never vary it. The same rule governs variable names and
instrument names.

---

## 7. Acronym pile-up

> **Before.** The LADCP and SADCP velocities were merged with the CTD data before
> the IBM was applied to estimate the MOC and the MHT.

Six acronyms in a sentence, two of them (IBM, MHT) not standard enough to pass
undefined, and *IBM* actively collides with a famous company.

> **After.** We merged lowered and shipboard ADCP velocities with the CTD data,
> then applied an inverse box model to estimate the overturning circulation and
> its heat transport.

Keep the acronyms a reader of the journal already knows — CTD, ADCP. Spell out
the ones you invented. An acronym used twice is not worth its definition.

---

## 8. Results that read the table aloud

> **Before.** The Canary Current transport was 3.1 ± 0.6 Sv in 1997, 2.8 ± 0.5 Sv
> in 2003, 3.4 ± 0.7 Sv in 2011 and 3.0 ± 0.6 Sv in 2016 (Table 2).

The table already says this. Prose that recites it wastes the one place where you
get to tell the reader what the numbers mean.

> **After.** Canary Current transport varied by less than 0.6 Sv across the four
> occupations, within the uncertainty of any single estimate (Table 2).

State the pattern and its significance; let the table hold the values.

---

## 9. Negatives, and a double negative

> **Before.** The transports are not inconsistent with previous estimates, and the
> residuals were not large.

*Not inconsistent* makes the reader reverse two negations to reach a positive.
*Not large* is vaguer than any number.

> **After.** The transports agree with previous estimates, and residuals stayed
> below 0.4 Sv.

Say what a thing is, not what it is not. If you mean *agree*, write *agree*.

---

## 10. Parallelism in a list of contributions

> **Before.** In this work we present new hydrographic data, the circulation is
> estimated using an inverse model, and comparison with reanalysis products.

Three items, three different grammatical shapes: a verb phrase, an independent
clause, a bare noun. The list reads as if something went missing.

> **After.** We present new hydrographic data, estimate the circulation with an
> inverse model, and compare the result with reanalysis products.

Three verbs in the same form. Parallel structure is not decoration — it tells the
reader the three items are of the same kind.

---

## 11. Where a figure beats a paragraph

> **Before.** The section runs eastward from the continental slope off Florida at
> approximately 27°N, crosses the Bahamas Bank, continues past the Mid-Atlantic
> Ridge at approximately 45°W, and terminates on the African slope near 15°W,
> with station spacing of 55 km over the boundaries and 110 km in the interior.

Nothing is wrong with the prose. But no reader builds an accurate map from it,
and every reader tries.

> **After.** A station map (Figure 1) with the spacing annotated, and one
> sentence: *The section spans 27°N from the Florida slope to the African slope,
> with station spacing halved over both boundaries.*

Geometry belongs in a figure. Prose should say what the geometry is *for*.
