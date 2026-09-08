# Grammar tips and keyword consistency

Source: modules 2.6, 3.7, 1.3.

None of the grammar points below will get a manuscript rejected. Getting them
right signals professionalism; getting them wrong signals sloppiness, and a
reviewer who has spotted sloppiness starts looking for more.

---

## 1. *Data* is plural

*The data **are**. The data **show**. These data **support**.* The singular is
*datum*, a single data point, which you almost never mean.

Most people get this wrong in speech and in writing, so it has to be learned
deliberately. After enough editing only the plural sounds right.

## 2. *Affect* vs *effect*

*Affect* with an **a** is the **verb**: to influence. *Effect* with an **e** is
the **noun**: the influence itself.

- *The class affected her.*
- *The class had an effect on her.*

Two exceptions, both rare. *Affect* as a noun means emotional expression, used
almost only in psychology. *Effect* as a verb means to bring about — *she effected
a change*. Your spell-checker will not catch a mix-up.

## 3. *Compared with* vs *compared to*

*Compared to* points out similarities between **different** things — the
metaphorical use. *Shall I compare thee to a summer's day?*

*Compared with* points out differences between **similar** things. In science
this is nearly always what you mean: two groups of mice, two tumours, two
algorithms.

> *Brain tumors are relatively rare compared **with** more common cancers such as
> those of the lung, breast, and prostate.*

## 4. *That* vs *which*

*That* introduces a **restrictive** (essential) clause and takes **no commas**.
*Which* introduces a **non-restrictive** (non-essential) clause and is **set off
by commas**.

The test: can you delete the clause without changing the meaning? If yes, it is
non-essential — commas and *which*. If no, *that*.

> *The vial **that** contained her RNA was lost.* — there are several vials; this
> clause identifies which one.
>
> *The vial, **which** contained her RNA, was lost.* — there is one vial; the RNA
> is an extra fact about it.

Real corrections:

> *Other disorders **which** have been found to co-occur with diabetes include heart disease and foot problems.*

The author used no commas, so they knew the clause was essential — it needs
*that*.

> *Stroke incidence data are obtained from sources, which use the ICD classification systems.*

Stop after *sources* and the sentence means nothing. The clause is essential:
drop the comma, use *that*.

Even Feynman got this wrong. Strunk and White: *careful writers, watchful for
small conveniences, go witch-hunting, remove the defining whiches, and by doing
so improve their work.*

## 5. Singular subject, plural pronoun

*Each student worries about their grade* is a disagreement. Fixing it with
*his/her* is clumsy, and choosing one gender is a choice you may not want to
make. The clean escape is to go plural:

> *All students worry about their grades.*

## 6. *Principle* vs *principal*

A spell-checker will not catch this either. *Principal* ends in **pal** — the
principal is your pal, the head of a school, or the main thing. *Principle* is a
fundamental tenet. *The final concentrations were in principle…* needs
*principle*.

---

## Keyword consistency — the banana rule

You were probably taught not to repeat a word. In scientific writing that advice
is actively harmful.

**Repeat your keywords.** Group names, variable names, instrument names, disease
names, technique names — these must be identical every time, in the Abstract, the
Methods, the Results, the Discussion, every table title, every column heading and
every figure legend.

If Methods says *obese group* and *lean group*, and Results says *heavier group*
and *lighter group*, the reader stops and asks: are these new groups? Were the
categories redefined? In prose that is merely confusing; in a manuscript it can
make the results unreadable.

**Where the impulse comes from.** You notice you have used a word four times, you
feel self-conscious, you open a thesaurus. Two better answers come first:

1. Do you need the second instance at all? Often the first carries over. (*…that
   illustrate challenges and solutions* — one *illustrate* serves both.)
2. If you do need it, is the synonym actually better than the repetition? Usually
   not.

**Elegant variation** is Fowler's name for this vice, and it produces genuinely
absurd prose. Real examples from professional writers, collected in *Time*:

- banana → *the elongated yellow fruit*
- beaver → *the furry, paddle-tailed mammal*
- mustache → *under-nose hair crops*
- milk from a cow → *the vitamin-laden liquid from a bovine milk factory*
- skis → *the beatified barrel staves*

Funny in a newspaper. In a paper, it is a reader wondering whether you have
introduced a second variable.

`keyword_consistency.py` detects this pattern across sections automatically.

---

## Acronym austerity

Acronyms spread because you get tired of typing the keyword. But every
non-standard acronym forces the reader to stop and translate a foreign word,
which is a heavy tax for a few saved characters.

**Rules:**

- Use only acronyms that are standard across science and widely known — DNA,
  RNA, CPU, FPGA, PSNR. Do not invent your own, and do not use ones that only
  your immediate subfield knows.
- Weigh the saving honestly. *microRNA* → *miR* saves five characters and costs
  the reader a lookup. (And *RNA* is already an acronym, so that one is an
  acronym of an acronym.)
- If an acronym is truly unavoidable, **define it in every section** — abstract,
  main text, and each table and figure legend separately. Readers do not read
  linearly; defining it once at the top is not enough.
- A used-three-times acronym is not worth having. Spell it out.

**The typing trick:** if you want an abbreviation while drafting to save
keystrokes, use one — then run find-and-replace before you submit and put the
words back. Your reader will thank you.

What it looks like when this goes wrong:

> *Spinal muscle fatigue is common in people with LLA, because decreased spinal
> muscle endurance and strength has been reported in persons with TFA and TTA
> with LBP.*

---

## Vague words and unnecessary jargon

A close relative of the acronym problem: words so broad the reader cannot form a
picture. *Physiologic* covers all of physiology. *Molecular species* could be
anything. *Gliomagenesis* is a longer way to say *the formation of glioma*.

Complex, technical ideas do not require complex language. You can convey them in
simple language, and if scientific writing did that, it would be far easier and
more enjoyable to read.
