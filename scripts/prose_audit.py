#!/usr/bin/env python3
"""Flag the mechanical defects that Writing in the Sciences teaches you to hunt.

This does the grep so the model can spend its attention on judgment. It finds
candidates; it does not decide. Every hit still needs a human or model read,
because most of these patterns have legitimate uses (passive voice in Methods,
a "to be" verb that is genuinely the right verb, a standard acronym).

Usage:
    python prose_audit.py draft.tex
    python prose_audit.py draft.tex --section discussion
    python prose_audit.py draft.md --json
    echo "some prose" | python prose_audit.py -

Checks, in the order the course teaches them:
    clutter      dead-weight openers, empty phrases, long-for-short, redundancy
    verbs        to-be verbs, passive voice, nominalisations, buried predicates
    negatives    "not X" that has a positive form
    expletives   superfluous "there is / there are"
    adverbs      -ly adverbs and the usual intensifiers
    acronyms     inventory, first use, whether each is worth its cost
    paragraphs   length, transition-word openers, sentence-length monotony
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# --------------------------------------------------------------------------
# Lexicons (module 1.4, 1.5, 2.4, 4.5)
# --------------------------------------------------------------------------

# Throat-clearing: the author warming up. Delete and let a citation carry it.
DEAD_WEIGHT = [
    r"as (?:it )?is well known", r"as (?:it )?has been (?:shown|demonstrated|reported)",
    r"it (?:can|should|must) be (?:regarded|noted|emphasi[sz]ed|mentioned|pointed out)",
    r"it is (?:worth|important|interesting|noteworthy|necessary) (?:to note|noting|to mention|mentioning)",
    r"it is (?:well[- ])?(?:known|established|documented) that",
    r"it should be (?:noted|stressed|highlighted)",
    r"needless to say", r"it goes without saying",
    r"in (?:my|our) opinion", r"to the best of (?:my|our) knowledge",
    r"as (?:we |one )?can (?:be )?see(?:n)? (?:from|in)",
    r"it is (?:generally|widely) (?:accepted|believed|agreed)",
    r"in this (?:paper|section|work),? we (?:will|shall) (?:now )?(?:present|describe|discuss)",
]

# Blobs: too vague to give the reader a picture (Zinsser's "some words are blobs").
EMPTY = [
    r"basic tenets of", r"a profile of", r"the (?:field|area|realm|domain) of",
    r"in terms of", r"with (?:regard|respect) to", r"in the context of",
    r"a (?:number|variety|range) of (?:different )?", r"various (?:different )?",
    r"the (?:process|procedure|task|act) of", r"the concept of", r"the nature of",
    r"the (?:presence|existence) of", r"in (?:this|that) regard",
    r"molecular species", r"physiologic(?:al)? ", r"methodologic(?:al)? ",
    r"the (?:occurrence|incidence) of", r"levels? of", r"type of",
]

# Long-for-short: same meaning, more words (module 1.4).
LONG_FOR_SHORT = {
    r"due to the fact that": "because",
    r"owing to the fact that": "because",
    r"in light of the fact that": "because",
    r"in view of the fact that": "because",
    r"despite the fact that": "although",
    r"in spite of the fact that": "although",
    r"notwithstanding the fact that": "although",
    r"in the event that": "if",
    r"in the case (?:that|where)": "if / when",
    r"based on the assumption that": "if",
    r"under (?:the )?circumstances in which": "when",
    r"at (?:the|this) (?:present|current) (?:time|moment)": "now",
    r"in (?:the )?close proximity to": "near",
    r"a majority of": "most",
    r"a (?:large|small) number of": "many / few",
    r"a number of": "several",
    r"the majority of": "most",
    r"are of the same opinion": "agree",
    r"is (?:in )?agreement with": "agrees with",
    r"less frequently occurring": "rare",
    r"give(?:s)? rise to": "causes",
    r"have an (?:effect|impact) on": "affect",
    r"has an (?:effect|impact) on": "affects",
    r"in order to": "to",
    r"for the purpose of": "to",
    r"with the aim of": "to",
    r"on the basis of": "from / based on",
    r"in the (?:absence|lack) of": "without",
    r"prior to": "before",
    r"subsequent to": "after",
    r"in close(?:r)? agreement": "agrees",
    r"it is possible that": "may",
    r"has (?:been|the ability) to": "can",
    r"is capable of": "can",
    r"an? (?:sufficient|adequate) (?:amount|quantity) of": "enough",
    r"the (?:vast )?majority": "most",
    r"utili[sz]e(?:s|d)?": "use",
    r"demonstrate(?:s|d)? that": "shows",
    r"is indicative of": "indicates",
    r"in a .{0,12}(?:manner|fashion|way)": "an adverb, or rewrite the verb",
    r"serve(?:s)? to": "(delete)",
    r"the neonatal population": "newborns",
    r"have (?:long )?been (?:known|estimated|shown) to be": "are",
}

# Adjective already inside the noun, or adverb already inside the verb.
REDUNDANT = [
    (r"successful solutions?", "a solution is by definition successful"),
    (r"completely eliminat", "eliminate is already complete"),
    (r"totally destroy", "destroy is already total"),
    (r"future plans?", "plans are about the future"),
    (r"past history", "history is past"),
    (r"unexpected surprise", "a surprise is unexpected"),
    (r"currently underway", "underway is current"),
    (r"end result", "a result is an end"),
    (r"final outcome", "an outcome is final"),
    (r"advance planning", "planning is in advance"),
    (r"basic fundamentals?", "fundamentals are basic"),
    (r"new innovation", "an innovation is new"),
    (r"close proximity", "proximity is closeness"),
    (r"absolutely essential", "essential is absolute"),
    (r"exactly identical", "identical is exact"),
    (r"first (?:ever )?of its kind and .{0,20}proof of principle",
     "first-of-its-kind and proof-of-principle say the same thing"),
]

# Weak verb + nominalised noun: the spunky verb turned into a boring noun (2.4).
SMOTHERED = [
    (r"\b(?:provide[sd]?|give[sn]?|offer(?:s|ed)?)\s+(?:an?\s+)?(?:review|overview|summary|description|analysis|assessment|explanation|discussion|comparison|estimate|indication|confirmation)\s+of\b", "use the verb: reviews / summarises / describes / analyses …"),
    (r"\bperform(?:s|ed)?\s+(?:an?\s+)?(?:analysis|assessment|evaluation|comparison|measurement|calculation|investigation)\s+of\b", "analyse / assess / evaluate / compare / measure / calculate"),
    (r"\bconduct(?:s|ed)?\s+(?:an?\s+)?(?:analysis|assessment|study|investigation|evaluation|comparison|survey)\s+of\b", "analyse / assess / study / investigate"),
    (r"\bcarr(?:y|ies|ied)\s+out\s+(?:an?\s+)?(?:analysis|measurement|investigation|comparison)\b", "analyse / measure / investigate / compare"),
    (r"\bmake[s]?\s+(?:an?\s+)?(?:adjustment|decision|comparison|contribution|assumption|modification|improvement)\b", "adjust / decide / compare / contribute / assume / modify / improve"),
    (r"\bobtain(?:s|ed)?\s+(?:an?\s+)?(?:estimate|measurement|value)s?\s+of\b", "estimate / measure"),
    (r"\bshow(?:s|ed|n)?\s+(?:an?\s+)?(?:peak|increase|decrease|reduction|improvement)\b", "peaks / increases / decreases / improves"),
    (r"\b(?:achieve|attain)(?:s|d)?\s+(?:an?\s+)?(?:reduction|increase|improvement)\s+(?:in|of)\b", "reduce / increase / improve"),
    (r"\bhas seen an? \w+ in\b", "use the verb directly"),
    (r"\bresult(?:s|ed)? in (?:the )?(?:activation|inhibition|recruitment|formation|reduction|increase|expression|degradation|production|generation)\s+of\b", "activates / inhibits / recruits / forms / reduces / increases / expresses …"),
    (r"\btake(?:s|n)? (?:an? )?(?:assessment|measurement|reading) of\b", "assess / measure / read"),
    (r"\bis (?:responsible for|involved in) the \w+(?:tion|ment|ance|ence|sion) of\b", "use the verb"),
]

# Nominalisation suffixes to count as a density signal.
NOMINAL_SUFFIX = re.compile(
    r"\b[a-z]{3,}(?:tion|sion|ment|ance|ence|ancy|ency|ity|ness|ization|isation|ysis)\b", re.I)

TO_BE = r"\b(?:is|are|was|were|be|been|being|am)\b"

# A passive verb is a "to be" form plus a past participle (module 2.1).
IRREGULAR_PP = (r"shown|seen|found|given|taken|made|done|known|held|kept|built|"
                r"put|set|led|felt|left|lost|meant|sent|spent|told|understood|"
                r"written|driven|grown|drawn|chosen|proven|born|brought|bought|"
                r"caught|thought|taught|sought|dealt|met|read|run|cut|hit|"
                r"undertaken|withdrawn|overcome|become")
PASSIVE = re.compile(
    r"\b(?:is|are|was|were|be|been|being|am)\b"
    r"(?:\s+(?:not|also|then|only|further|already|subsequently|previously|"
    r"clearly|therefore|thus|generally|typically|usually|often|(?:\w+ly)))?"
    r"\s+(\w+ed|" + IRREGULAR_PP + r")\b", re.I)

# "was interested", "is based" etc. are stative and usually fine.
PASSIVE_BENIGN = {"based", "interested", "located", "situated", "composed", "comprised",
                  "concerned", "involved", "related", "associated", "aimed", "intended",
                  "supposed", "expected", "required", "limited", "restricted", "defined"}

EXPLETIVE = re.compile(r"\bthere\s+(?:is|are|was|were|has been|have been|exists?|exist)\b", re.I)

NEGATIVES = {
    r"\bnot\s+(?:very\s+)?often\b": "rarely / usually not",
    r"\bdoes not have\b": "lacks",
    r"\bdo not have\b": "lack",
    r"\bdid not have\b": "lacked",
    r"\bdid not remember\b": "forgot",
    r"\bdid not (?:pay attention to|consider)\b": "ignored / overlooked",
    r"\bdid not succeed\b": "failed",
    r"\bnot (?:honest|truthful)\b": "dishonest",
    r"\bnot harmful\b": "safe",
    r"\bnot important\b": "unimportant",
    r"\bnot (?:possible|feasible)\b": "impossible",
    r"\bnot (?:sufficient|enough)\b": "insufficient",
    r"\bnot (?:significant|significantly different)\b": "similar (if that is what you mean)",
    r"\bnot (?:able|capable)\b": "unable",
    r"\bnot (?:clear|obvious)\b": "unclear",
    r"\bnot the same\b": "different",
    r"\bnot (?:present|detected)\b": "absent / undetected",
    r"\bdid not (?:differ|change)\b": "was unchanged / similar",
    r"\bnot (?:common|frequent)\b": "rare",
    r"\bnot (?:correct|right)\b": "wrong / incorrect",
}

INTENSIFIERS = {"very", "really", "quite", "basically", "generally", "actually",
                "essentially", "fundamentally", "extremely", "highly", "greatly",
                "significantly", "considerably", "substantially", "clearly",
                "obviously", "certainly", "definitely", "particularly", "notably",
                "relatively", "somewhat", "rather", "fairly", "truly", "simply",
                "merely", "just", "totally", "completely", "entirely", "absolutely"}

# The course asks for "but" and "and". Everything else is usually a crutch (3.4).
TRANSITIONS = {"however", "nevertheless", "nonetheless", "furthermore", "moreover",
               "therefore", "thus", "hence", "consequently", "additionally",
               "accordingly", "conversely", "similarly", "likewise", "indeed",
               "interestingly", "importantly", "notably", "subsequently",
               "in addition", "on the other hand", "in contrast", "as a result",
               "for this reason", "in conclusion", "to this end"}

STANDARD_ACRONYMS = {
    "DNA", "RNA", "MRNA", "PCR", "ATP", "ADP", "PH", "UV", "IR", "MRI", "CT", "EEG",
    "ECG", "HIV", "AIDS", "USA", "US", "UK", "EU", "WHO", "NIH", "NASA", "IEEE",
    "CPU", "GPU", "RAM", "ROM", "USB", "PDF", "HTML", "XML", "JSON", "API", "OS",
    "AI", "ML", "SNR", "RMS", "DC", "AC", "LED", "LCD", "PID", "FFT", "PWM", "I2C",
    "SPI", "UART", "ADC", "DAC", "FPGA", "ASIC", "SOC", "GPIO", "DDR", "SDK", "IDE",
    "CFD", "FEM", "FEA", "PIV", "SEM", "TEM", "XRD", "NMR", "GPS", "RF", "SD", "CI",
    "3D", "2D", "1D", "ANOVA", "SD", "SEM", "CI", "OR", "RR", "HR", "BMI",
}
ACRONYM_RE = re.compile(r"\b(?:[0-9]?[A-Z]{2,}[0-9]*|[A-Z][a-z]?[A-Z]{1,}[0-9]*)\b")

SENT_SPLIT = re.compile(r"(?<=[.!?])[\"')\]]*\s+(?=[A-Z(\"'\[])")


# --------------------------------------------------------------------------

def split_sentences(text):
    """Return (sentence, char_offset) pairs, protecting common abbreviations."""
    protected = text
    for abbr in ["e.g.", "i.e.", "et al.", "vs.", "cf.", "Fig.", "Eq.", "Ref.",
                 "Dr.", "Prof.", "approx.", "ca.", "no.", "No.", "Sec.", "Tab.",
                 "Table.", "min.", "max.", "etc."]:
        protected = protected.replace(abbr, abbr.replace(".", "\x00"))
    out, start = [], 0
    for m in SENT_SPLIT.finditer(protected):
        out.append((protected[start:m.start()].replace("\x00", "."), start))
        start = m.end()
    tail = protected[start:].replace("\x00", ".").strip()
    if tail:
        out.append((tail, start))
    return [(s.strip(), o) for s, o in out if s.strip()]


def word_count(s):
    return len(re.findall(r"\b[\w'-]+\b", s))


def line_of(text, offset):
    return text.count("\n", 0, offset) + 1


def excerpt(sentence, limit=110):
    s = " ".join(sentence.split())
    return s if len(s) <= limit else s[:limit - 1] + "…"


def subject_verb_distance(sentence):
    """Rough words before the main verb — the 'buried predicate' signal (2.4).

    Approximate on purpose: a real parse is not worth the dependency, and the
    number is only ever a prompt to look, never a verdict.
    """
    words = re.findall(r"\b[\w'-]+\b", sentence)
    verb_cue = re.compile(
        r"^(?:is|are|was|were|be|been|being|am|has|have|had|do|does|did|"
        r"can|could|will|would|shall|should|may|might|must|"
        r"show|shows|showed|found|find|finds|report|reports|reported|"
        r"suggest|suggests|suggested|demonstrate|demonstrates|demonstrated|"
        r"indicate|indicates|indicated|reveal|reveals|revealed|"
        r"increase[sd]?|decrease[sd]?|remain(?:s|ed)?|appear(?:s|ed)?|"
        r"provide[sd]?|include[sd]?|require[sd]?|allow(?:s|ed)?|"
        r"occur(?:s|red)?|exist(?:s|ed)?|yield(?:s|ed)?|contain(?:s|ed)?)$", re.I)
    # A leading subordinate clause resets the count; only look after the comma.
    for i, w in enumerate(words):
        if verb_cue.match(w):
            return i, w
    return None, None


# --------------------------------------------------------------------------

def audit(text, label=""):
    findings = defaultdict(list)
    sentences = split_sentences(text)

    def add(kind, sent, off, message, match=None, fix=None):
        findings[kind].append({
            "line": line_of(text, off),
            "match": match,
            "fix": fix,
            "note": message,
            "sentence": excerpt(sent),
        })

    for sent, off in sentences:
        low = sent.lower()

        for pat in DEAD_WEIGHT:
            for m in re.finditer(pat, low):
                add("clutter", sent, off, "throat-clearing — delete and let a citation carry it",
                    match=m.group(0), fix="(delete)")

        for pat in EMPTY:
            for m in re.finditer(pat, low):
                add("clutter", sent, off, "vague filler — gives the reader no picture",
                    match=m.group(0), fix="(delete or be specific)")

        for pat, repl in LONG_FOR_SHORT.items():
            for m in re.finditer(pat, low):
                add("clutter", sent, off, "long where short would do",
                    match=m.group(0), fix=repl)

        for pat, why in REDUNDANT:
            for m in re.finditer(pat, low):
                add("clutter", sent, off, why, match=m.group(0), fix="(cut the modifier)")

        for pat, fix in SMOTHERED:
            for m in re.finditer(pat, low):
                add("verbs", sent, off, "smothered verb — a strong verb turned into a noun",
                    match=" ".join(m.group(0).split()), fix=fix)

        for m in PASSIVE.finditer(sent):
            pp = m.group(1).lower()
            if pp in PASSIVE_BENIGN:
                continue
            add("verbs", sent, off,
                "passive — ask 'who does what to whom?'; fine in Methods, costly elsewhere",
                match=" ".join(m.group(0).split()), fix="(active, or keep deliberately)")

        tobe = [m.group(0) for m in re.finditer(TO_BE, low)]
        if len(tobe) >= 2 and word_count(sent) < 45:
            add("verbs", sent, off,
                "%d 'to be' verbs in one sentence — at least one is doing no work" % len(tobe),
                match=", ".join(tobe))

        dist, verb = subject_verb_distance(sent)
        if dist is not None and dist >= 12:
            add("verbs", sent, off,
                "buried predicate: %d words before the main verb ('%s'); readers wait for the verb"
                % (dist, verb), match=verb, fix="move the verb up, set the description aside in commas")

        for pat, fix in NEGATIVES.items():
            for m in re.finditer(pat, low):
                add("negatives", sent, off, "state it positively — usually clearer",
                    match=m.group(0), fix=fix)
        negs = re.findall(
            r"\b(?:not|no|never|neither|nor|without|fail(?:s|ed)? to|lack(?:s|ed|ing)?|"
            r"un(?:able|clear|likely|common|changed|expected|successful|necessary|"
            r"detected|related|affected|known|certain)\w*|"
            r"in(?:correct|complete|sufficient|adequate|consistent|valid|frequent|"
            r"significant|accurate|appropriate)\w*|"
            r"im(?:possible|proper|precise)\w*|non-?\w+)\b", low)
        if len(negs) >= 2:
            add("negatives", sent, off,
                "%d negatives in one sentence — a double negative makes the reader do algebra"
                % len(negs), match=", ".join(negs), fix="state it positively")

        for m in EXPLETIVE.finditer(sent):
            add("expletives", sent, off,
                "'there is/are' usually hides a better verb", match=m.group(0),
                fix="rewrite around the real subject")

        for m in re.finditer(r"\b(\w+ly)\b", low):
            w = m.group(1)
            if w in {"only", "early", "likely", "family", "supply", "apply", "reply",
                     "multiply", "assembly", "anomaly", "italy", "july"}:
                continue
            severity = "intensifier — almost never adds power" if w in INTENSIFIERS \
                else "adverb — check whether a better verb absorbs it"
            add("adverbs", sent, off, severity, match=w, fix="(cut, or pick a stronger verb)")

    # ---- acronyms -------------------------------------------------------
    seen_first = {}
    counts = Counter()
    for sent, off in sentences:
        for m in ACRONYM_RE.finditer(sent):
            a = m.group(0)
            if a.isdigit() or len(a) > 8:
                continue
            counts[a] += 1
            if a not in seen_first:
                # Defined if the sentence has "Full Words (ACR)" or "ACR (full words)".
                window = sent[max(0, m.start() - 90):m.end() + 90]
                defined = bool(re.search(r"\([^)]*\b" + re.escape(a) + r"\b[^)]*\)", window)) or \
                          bool(re.search(re.escape(a) + r"\s*\([A-Za-z][^)]{3,}\)", window))
                seen_first[a] = {"line": line_of(text, off), "defined": defined,
                                 "sentence": excerpt(sent)}
    for a, info in sorted(seen_first.items(), key=lambda kv: -counts[kv[0]]):
        if a in STANDARD_ACRONYMS:
            continue
        n = counts[a]
        note = []
        if not info["defined"]:
            note.append("not defined at first use")
        if n <= 3:
            note.append("used only %d time%s — spell it out and drop the acronym" % (n, "" if n == 1 else "s"))
        if note:
            findings["acronyms"].append({
                "line": info["line"], "match": a, "fix": None,
                "note": "; ".join(note) + " (uses: %d)" % n,
                "sentence": info["sentence"],
            })

    # ---- paragraphs -----------------------------------------------------
    for para in re.finditer(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", text):
        block = para.group(0).strip()
        if word_count(block) < 25:
            continue
        off = para.start()
        sents = split_sentences(block)
        lengths = [word_count(s) for s, _ in sents]
        if len(sents) > 6:
            findings["paragraphs"].append({
                "line": line_of(text, off), "match": None, "fix": "split it",
                "note": "%d sentences — a paragraph carries one idea; professional prose runs 2-5"
                        % len(sents),
                "sentence": excerpt(sents[0][0]),
            })
        starters = [s.strip().split(",")[0].lower() for s, _ in sents]
        hits = [s for s in starters if s.split()[0].strip(".,;:") in TRANSITIONS
                or s in TRANSITIONS]
        if len(hits) >= 2:
            findings["paragraphs"].append({
                "line": line_of(text, off), "match": ", ".join(hits), "fix": "use 'but' and 'and', or fix the logic",
                "note": "%d of %d sentences open with a transition word — usually a sign the "
                        "underlying logic is doing the work it should" % (len(hits), len(sents)),
                "sentence": excerpt(sents[0][0]),
            })
        if len(lengths) >= 4 and max(lengths) - min(lengths) <= 6:
            findings["paragraphs"].append({
                "line": line_of(text, off), "match": None, "fix": "vary with a colon, dash or semicolon",
                "note": "all %d sentences are %d-%d words — monotonous rhythm"
                        % (len(lengths), min(lengths), max(lengths)),
                "sentence": excerpt(sents[0][0]),
            })

    # ---- summary --------------------------------------------------------
    total_words = word_count(text)
    lengths = [word_count(s) for s, _ in sentences]
    nominals = len(NOMINAL_SUFFIX.findall(text))
    summary = {
        "label": label,
        "words": total_words,
        "sentences": len(sentences),
        "mean_sentence_words": round(sum(lengths) / len(lengths), 1) if lengths else 0,
        "longest_sentence_words": max(lengths) if lengths else 0,
        "nominalisation_density_per_100w": round(100 * nominals / total_words, 1) if total_words else 0,
        "to_be_density_per_100w": round(100 * len(re.findall(TO_BE, text, re.I)) / total_words, 1) if total_words else 0,
        "passive_count": len(findings["verbs"]) and sum(
            1 for f in findings["verbs"] if f["note"].startswith("passive")),
        "counts": {k: len(v) for k, v in sorted(findings.items())},
    }
    return summary, dict(findings)


# --------------------------------------------------------------------------

ORDER = ["clutter", "verbs", "negatives", "expletives", "adverbs", "acronyms", "paragraphs"]
TITLES = {
    "clutter": "CLUTTER — strip every sentence to its cleanest components",
    "verbs": "VERBS AND VOICE — verbs drive sentences; nouns slow them down",
    "negatives": "NEGATIVES — say what a thing is, not what it is not",
    "expletives": "THERE IS / THERE ARE — a better verb is usually hiding underneath",
    "adverbs": "ADVERBS — you lose power by adding them, not gain it",
    "acronyms": "ACRONYMS — every undefined one makes the reader translate a foreign word",
    "paragraphs": "PARAGRAPHS — one idea each, and let logic carry the flow",
}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="manuscript file, or - for stdin")
    ap.add_argument("--section", help="audit only this section (needs extract_text.py)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--max-per-check", type=int, default=25,
                    help="cap hits printed per check (default 25)")
    args = ap.parse_args()

    if args.path == "-":
        text, label = sys.stdin.read(), "stdin"
    else:
        suffix = Path(args.path).suffix.lower()
        if suffix in (".tex", ".docx", ".md", ".markdown") or args.section:
            import extract_text
            secs = extract_text.extract(args.path)
            if args.section:
                q = args.section.lower()
                hit = next((s for s in secs
                            if q in s["heading"].lower() or (s["canonical"] and q in s["canonical"])), None)
                if not hit:
                    sys.exit("No section matched %r. Available: %s"
                             % (args.section, ", ".join(s["heading"] for s in secs)))
                text, label = hit["text"], hit["heading"]
            else:
                text = "\n\n".join(s["text"] for s in secs if s["text"])
                label = Path(args.path).name
        else:
            text, label = Path(args.path).read_text(encoding="utf-8", errors="replace"), Path(args.path).name

    summary, findings = audit(text, label)

    if args.json:
        print(json.dumps({"summary": summary, "findings": findings},
                         ensure_ascii=False, indent=2))
        return

    print("=" * 78)
    print("PROSE AUDIT — %s" % (label or "input"))
    print("=" * 78)
    print("%d words · %d sentences · mean %.1f words · longest %d words"
          % (summary["words"], summary["sentences"],
             summary["mean_sentence_words"], summary["longest_sentence_words"]))
    print("nominalisations %.1f per 100 words · 'to be' verbs %.1f per 100 words"
          % (summary["nominalisation_density_per_100w"], summary["to_be_density_per_100w"]))
    print()

    if not findings:
        print("No mechanical flags. Judgment work remains: logic, structure, and whether")
        print("each paragraph carries one idea.")
        return

    for kind in ORDER:
        hits = findings.get(kind)
        if not hits:
            continue
        print("-" * 78)
        print("%s   (%d)" % (TITLES[kind], len(hits)))
        print("-" * 78)
        for f in hits[:args.max_per_check]:
            head = "  L%-5d" % f["line"]
            if f["match"]:
                head += " %-42s" % ("«%s»" % f["match"])
            print(head)
            print("         %s" % f["note"])
            if f["fix"]:
                print("         → %s" % f["fix"])
            print("         %s" % f["sentence"])
            print()
        if len(hits) > args.max_per_check:
            print("  … %d more\n" % (len(hits) - args.max_per_check))

    print("=" * 78)
    print("These are candidates, not verdicts. Passive voice and jargon are legitimate")
    print("in Methods; a repeated keyword is mandatory everywhere. Read before you cut.")


if __name__ == "__main__":
    main()
