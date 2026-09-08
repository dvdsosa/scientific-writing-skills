# Contributing

Thanks for considering it. This project has an unusual quality bar: **the rules
must match the source**. A change that makes the plugin more useful but
misrepresents what the course teaches is not an improvement.

## The one rule

Every instruction in a `SKILL.md` or a `references/*.md` file must be
**traceable to a module of Writing in the Sciences** — cite it (`module 3.4`).

The exception is material clearly labelled as not from the course, which today
means `engineering-examples.md` and `oceanography-examples.md`: the rules there
are the course's, the sentences are ours, and each file says so at the top. If you add a rule you believe is good
practice but cannot cite, it needs the same treatment — say plainly where it came
from, so a reader can tell the course's authority from ours.

## Especially welcome

**Corrections against the source.** If a rule here misstates the course, that is
a bug and the highest-value contribution. Cite the module.

**Worked before/after pairs from your own field.** The course's examples are
biomedical; `engineering-examples.md` adds embedded systems and computer vision,
and `oceanography-examples.md` adds hydrography and ocean circulation. Chemistry,
ecology, economics, pure mathematics — all would help. Follow the existing format:
the flawed sentence, a diagnosis naming the rules involved, the rewrite, and what
was gained. Mark clearly that the sentences are yours and the rules are the
course's.

**False positives in the audit scripts.** If `prose_audit.py` flags something
legitimate, open an issue with the sentence. The scripts are deliberately
generous — they surface candidates and let the model judge — but a pattern that
is *usually* wrong to flag should be narrowed.

**Translations of the reference files.** The skills answer in the user's
language, but the reference material is English-only. Translated references
would help non-native speakers considerably. Keep the course's own example
sentences in their original English.

## Style

The reference files are written to be read by a model *and* by a person. That
means:

- Explain why a rule exists, not just what it is. Instructions that carry their
  reasoning survive paraphrase; bare imperatives do not.
- Prefer a worked example to an abstract statement of a principle.
- No ALL-CAPS MUSTs. If a rule needs shouting, it needs explaining.
- The skills' own advice applies to the skills' own prose. Cut the clutter.

## Scripts

- Standard library only. No dependencies, so anyone can run them anywhere.
- Python 3.8+.
- Every check needs a comment saying which module it comes from.
- Add a test case to the fixtures when you add a check.

## Pull requests

Keep them focused. A PR that fixes one false positive is easy to merge; a PR that
restructures three skills is not.

Run the scripts against the fixture files before submitting, and against a real
manuscript if you have one.
