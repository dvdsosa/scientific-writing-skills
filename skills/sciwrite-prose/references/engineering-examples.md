# Worked edits in engineering and computer vision

The course's own examples are biomedical. These apply the same rules to
embedded systems, FPGA design, signal processing and computer vision, so the
patterns are recognisable in that register.

**Provenance:** the *rules* come from the course; these *sentences* do not. They
were written to exercise the same defects in a different vocabulary. Cite the
course for the principle, not for these examples.

---

## 1. Clutter, nominalisation and a smothered verb

> **Before.** As it is well known, the implementation of a hardware acceleration
> strategy provides a reduction in the inference latency of convolutional neural
> networks that are deployed on resource-constrained embedded platforms.

Diagnosis: throat-clearing opener; *the implementation of* is a nominalisation;
*provides a reduction in* is a smothered verb (*reduces*); *resource-constrained*
and *embedded* are doing the same job; the main verb sits fifteen words in.

> **After.** Hardware acceleration reduces inference latency for convolutional
> networks on embedded platforms [refs].

24 words → 12, and the citation carries "as is well known" at no cost.

---

## 2. Passive voice hiding the actor

> **Before.** The bitstream was generated using Vivado 2022.1 and it was then
> loaded onto the KV260 board, where the measurements were taken.

Diagnosis: three passives in one sentence. In Methods, passive is legitimate —
what was done matters more than who did it, and this reads acceptably. But the
last clause is doing something different: *the measurements were taken* is vague
about *what* was measured, which the passive let the author skip.

> **After (Methods, passive kept).** The bitstream was generated in Vivado 2022.1
> and loaded onto the KV260 board. End-to-end latency was measured over 1,000
> frames.

> **After (Results, active).** We measured end-to-end latency over 1,000 frames.

The rule is not "no passive". It is: know why it is there. Here the fix was not
the voice, it was the missing object.

---

## 3. Cause and effect inverted by the passive

> **Before.** A degradation of the detection accuracy is caused by the
> quantisation of the network weights to eight-bit integers.

Diagnosis: the passive puts the effect first and the cause last, and buries two
verbs in nouns (*degradation*, *quantisation*).

> **After.** Quantising the weights to eight-bit integers degrades detection
> accuracy.

18 words → 10. Cause now precedes effect, and both nouns are verbs again.

---

## 4. Buried predicate

> **Before.** The proposed pipeline for real-time defect detection, which
> combines a lightweight backbone with a hardware-accelerated non-maximum
> suppression stage running on the programmable logic of the Kria KV260, achieves
> 31 frames per second at 1080p.

Diagnosis: twenty-six words between subject and *achieves*. The reader is holding
a long noun phrase with no idea where it is going.

> **After.** The proposed pipeline achieves 31 frames per second at 1080p by
> combining a lightweight backbone with hardware-accelerated non-maximum
> suppression on the KV260's programmable logic.

Nothing was cut except *for real-time defect detection*, which the section title
already established. The verb simply moved up.

**The licensed alternative** — a dash lets you keep the original order, because
the reader finds the verb the moment the dash closes:

> The proposed pipeline — a lightweight backbone plus hardware-accelerated
> non-maximum suppression on the KV260's programmable logic — achieves 31 frames
> per second at 1080p.

---

## 5. *There is*, and the verb hiding underneath

> **Before.** There is a significant increase in memory pressure when the batch
> size is raised above four.

> **After.** Memory pressure rises sharply above a batch size of four.

*There is … increase* became *rises*. Reserve *significant* for its statistical
sense; if you mean "large", say large.

---

## 6. Keyword drift across sections

> **Methods.** Frames were captured by the MIPI CSI-2 sensor and written to the
> DDR buffer.
>
> **Results.** Images acquired from the camera module showed a mean transfer time
> of 4.2 ms to the memory region.

Diagnosis: *frames* → *images*, *MIPI CSI-2 sensor* → *camera module*, *DDR
buffer* → *memory region*. Three renamings in one sentence. A reader now
reasonably wonders whether Results describes a different acquisition path.

> **Results, fixed.** Frames captured by the MIPI CSI-2 sensor reached the DDR
> buffer in 4.2 ms on average.

Repeating a keyword is not a stylistic failure. It is what tells the reader you
are still talking about the same thing.

---

## 7. Acronym pile-up

> **Before.** The DPU IP was integrated into the PL via AXI4, and the PS ran a
> PetaLinux image with the XRT stack managing DMA transfers between DDR and BRAM.

Diagnosis: seven acronyms in one sentence, of which DPU, PL, PS, XRT and BRAM are
not standard outside Xilinx work. A reader from an adjacent field is translating
nearly every word.

> **After.** The deep-learning processing unit (DPU) was integrated into the
> programmable logic over AXI4. The processor cores ran a PetaLinux image, and
> the Xilinx runtime managed transfers between external DDR memory and on-chip
> block RAM.

Longer in words, far shorter in reader effort — and split into two sentences,
because one was carrying two ideas.

---

## 8. Results that read the table aloud

> **Before.** Table 3 shows the performance of the three configurations. The mean
> latency of configuration A was 12.4 ± 1.3 ms, the mean latency of configuration
> B was 9.8 ± 1.1 ms, and the mean latency of configuration C was 9.6 ± 1.4 ms.
> The accuracy of configuration A was 91.2 %, of configuration B 93.7 %, and of
> configuration C 93.9 %.

Diagnosis: the reader has the table. Reading it back line by line adds nothing
and buries the finding.

> **After.** Hardware acceleration cut latency by roughly a quarter with no loss
> of accuracy; the two accelerated configurations were indistinguishable from
> each other (Table 3).

The one number worth pulling into the text is the one the study exists to
estimate. Everything else stays in the table.

---

## 9. Negatives, and a double negative

> **Before.** The results were not inconsistent with those reported for
> comparable architectures, and the overhead was not significant.

> **After.** The results agree with those reported for comparable architectures,
> and the overhead was small (2 % of total runtime).

*Not inconsistent* makes the reader do algebra. *Not significant* is worse: it is
ambiguous between the statistical sense and "small", so say which you mean and
give the number.

---

## 10. Parallelism in a list of contributions

> **Before.** The contributions of this work are: (1) a novel quantisation
> scheme; (2) we evaluate three backbones; (3) the release of an open dataset;
> and (4) showing that latency scales linearly with resolution.

Diagnosis: noun phrase, then a full clause, then a nominalisation, then a
gerund. Four structures in four items.

> **After (all noun phrases).** This work contributes a quantisation scheme for
> depthwise-separable layers, an evaluation of three backbones on the KV260, an
> open dataset of 4,000 annotated frames, and evidence that latency scales
> linearly with input resolution.

> **After (all verbs).** We introduce a quantisation scheme for
> depthwise-separable layers, evaluate three backbones on the KV260, release an
> open dataset of 4,000 annotated frames, and show that latency scales linearly
> with input resolution.

Either is fine. Mixing them is not.

---

## 11. Where a diagram beats a paragraph

> **Before.** Input frames are received by the capture stage, which forwards them
> to the pre-processing block; the pre-processing block resizes and normalises
> each frame before passing it to the inference engine, whose output is consumed
> by the post-processing stage, which in turn performs non-maximum suppression
> and writes the resulting bounding boxes back to the output buffer, from which
> the display stage reads them.

You can follow this, but only by rebuilding the diagram in your head — which is
the author asking the reader to do the author's work. A five-box flow diagram
conveys it instantly, and frees the prose to say the thing a diagram cannot:
which stage dominates the latency budget, and why.

> **After.** Figure 2 shows the pipeline. Inference dominates the latency budget
> (78 % of the per-frame total); the two hardware-accelerated stages together
> account for under 5 %.
