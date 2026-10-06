#!/usr/bin/env python3
"""Catch terminology drift between sections — the "banana rule" check.

Module 3.7 of Writing in the Sciences: in scientific writing, repeating a
keyword is not a sin, it is a requirement. If Methods says "obese group" and
Results says "heavier group", the reader stops to ask whether the categories
were redefined. Journalists calling a banana "the elongated yellow fruit" is
merely funny; doing it to a variable name is destructive.

This finds two things a reader would notice and an author never does:

  1. Terms that appear in one section and vanish in another where a
     near-synonym shows up instead.
  2. Acronyms that are defined once and then reused in later sections,
     tables or figure captions without redefinition — readers do not read
     linearly, so each section has to stand on its own.

Usage:
    python keyword_consistency.py paper.tex
    python keyword_consistency.py paper.tex --json
    python keyword_consistency.py paper.tex --terms "obese group,control arm,PSNR"
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract_text  # noqa: E402

STOP = set("""
a an the and or but if then than that this these those of in on at to for with
from by as is are was were be been being am do does did have has had not no
we our us they their it its he she his her you your i me my one two three
which who whom whose what when where why how all any both each few more most
other some such only own same so too very can will just should now also
between during before after above below over under again further here there
however therefore thus while although because since via using used use uses
based show shows showed found find figure table section chapter et al fig eq
respectively significant significantly result results method methods study
studies data value values case cases number time times high low large small
different similar new first second third performed obtained observed reported
""".split())

# Word-level synonym families that show up as drift in real manuscripts.
FAMILIES = [
    {"obese", "overweight", "heavier", "heavy", "adipose", "fat"},
    {"lean", "thin", "lighter", "normal-weight", "slim"},
    {"group", "arm", "cohort", "set", "population", "sample"},
    {"participant", "subject", "patient", "volunteer", "respondent"},
    {"treatment", "intervention", "therapy", "active"},
    {"control", "placebo", "sham", "baseline", "reference"},
    {"accuracy", "precision", "correctness", "exactness"},
    {"latency", "delay", "lag", "response-time"},
    {"throughput", "bandwidth", "rate", "speed"},
    {"device", "board", "platform", "hardware", "system", "unit", "module"},
    {"algorithm", "method", "approach", "technique", "procedure", "scheme"},
    {"image", "frame", "picture", "capture", "shot"},
    {"detection", "identification", "recognition", "localisation", "localization"},
    {"error", "deviation", "discrepancy", "mismatch", "residual"},
    {"increase", "rise", "growth", "gain", "improvement"},
    {"decrease", "reduction", "drop", "decline", "fall"},
]

ACRONYM_RE = re.compile(r"\b(?:[0-9]?[A-Z]{2,}[0-9]*|[A-Z][a-z]?[A-Z]{1,}[0-9]*)\b")

# Ordinary words that appear capitalised in headings, table cells and sentence
# starts. Without this they are reported as undefined acronyms.
NOT_ACRONYMS = {
    "IN", "IS", "AS", "AT", "OF", "TO", "OR", "AND", "THE", "WE", "IT", "ON",
    "BY", "NO", "SO", "IF", "ALL", "NOT", "FOR", "BUT", "ONE", "TWO", "NEW",
    "USE", "SEE", "VS", "ETC", "IE", "EG", "PER", "VIA", "END", "TOP", "LOW",
    "HIGH", "BEST", "MEAN", "SD", "SE", "MIN", "MAX", "AVG", "STD", "REF",
}

# Never expanded by anyone: brand names, product families, file formats,
# electrical and memory standards, and units. Flagging these is pure noise.
STANDARD = {
    # life sciences
    "DNA", "RNA", "PCR", "ATP", "HIV", "AIDS", "MRI", "CT", "EEG", "ECG", "BMI",
    # places and bodies
    "USA", "US", "UK", "EU", "WHO", "NIH", "IEEE", "ISO", "ACM", "NASA", "MDPI",
    # computing generalities
    "CPU", "GPU", "TPU", "NPU", "RAM", "ROM", "USB", "PCI", "PCIE", "HDMI",
    "PDF", "HTML", "XML", "JSON", "YAML", "CSV", "API", "SDK", "IDE", "OS",
    "AI", "ML", "DL", "CNN", "RNN", "LSTM", "GAN", "MLP", "SGD", "GUI", "CLI",
    "HTTP", "HTTPS", "TCP", "IP", "SSH", "URL", "URI", "UUID", "ASCII", "UTF",
    # vendors and product families
    "AMD", "NVIDIA", "INTEL", "ARM", "XILINX", "CUDA", "TENSORRT", "OPENCL",
    "OPENCV", "PYTORCH", "ONNX", "RISC", "CISC", "X86",
    # hardware, memory and electrical
    "FPGA", "ASIC", "SOC", "MPSOC", "GPIO", "DDR", "DDR3", "DDR4",
    "LPDDR", "LPDDR4", "SDRAM", "SRAM", "DRAM", "BRAM", "URAM", "FIFO", "DMA",
    "AXI", "I2C", "SPI", "UART", "ADC", "DAC", "PWM", "PLL", "LED", "LCD",
    "CMOS", "CCD", "MIPI", "CSI", "JTAG", "VDD", "VSS", "GND", "DC", "AC",
    "RF", "IR", "UV", "LUT", "DSP", "PS", "PL",
    # methods and metrics in common use
    "FFT", "DFT", "PID", "CFD", "FEM", "FEA", "PIV", "SEM", "TEM", "XRD", "NMR",
    "GPS", "IMU", "SNR", "RMS", "MSE", "RMSE", "MAE", "PSNR", "SSIM", "IOU",
    "ANOVA", "CI", "OR", "RR", "HR", "FPS", "FLOPS", "GFLOPS", "TOPS",
    # dimensions and units
    "1D", "2D", "3D", "4D", "MB", "GB", "KB", "TB", "MHZ", "GHZ", "KHZ",
}

# Sections whose vocabulary must agree; abstract counts, references do not.
CORE = {"abstract", "introduction", "methods", "results", "discussion", "conclusion"}


def ngrams(text, n):
    words = re.findall(r"\b[a-z][\w-]*\b", text.lower())
    for i in range(len(words) - n + 1):
        chunk = words[i:i + n]
        if any(w in STOP for w in chunk):
            continue
        if any(len(w) < 3 for w in chunk):
            continue
        yield " ".join(chunk)


def family_of(word):
    for i, fam in enumerate(FAMILIES):
        if word in fam:
            return i
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--terms", help="comma-separated terms you know are keywords; "
                                    "their absence from a section is reported explicitly")
    ap.add_argument("--min-count", type=int, default=2,
                    help="a phrase must appear this often overall to count as a keyword (default 3)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="report every core section that lacks its own definition of an "
                         "acronym (old, noisier behaviour), instead of just never-defined, "
                         "used-before-defined, abstract-only, and low-use acronyms")
    args = ap.parse_args()

    secs = extract_text.extract(args.path)
    named = [s for s in secs if s["text"].strip()]
    if not named:
        sys.exit("No text extracted from %s" % args.path)

    # Merge sections that share a canonical name (multi-part Methods, etc.).
    buckets = defaultdict(str)
    order = []
    for s in named:
        key = s["canonical"] or s["heading"]
        if key not in buckets:
            order.append(key)
        buckets[key] += "\n" + s["text"]
    core_keys = [k for k in order if k in CORE]
    if len(core_keys) < 2:
        core_keys = order  # not an IMRaD document; compare what is there

    report = {"sections": core_keys, "keyword_drift": [], "term_coverage": [],
              "acronyms": [], "synonym_pairs": []}

    # ---- 1. keyword phrases present in some sections and missing in others
    phrase_sec = defaultdict(set)
    phrase_count = Counter()
    for key in core_keys:
        text = buckets[key]
        for n in (2, 3):
            for g in set(ngrams(text, n)):
                phrase_sec[g].add(key)
        for g in ngrams(text, 2):
            phrase_count[g] += 1
        for g in ngrams(text, 3):
            phrase_count[g] += 1

    # Drift looks like this: two phrases differing in exactly one word, where that
    # word pair is a known synonym family or is near-identical, and the two phrases
    # live in *different* sections. Same-section use of both is fine — that is
    # ordinary prose variety within one passage, not a redefinition risk.
    candidates = [p for p, c in phrase_count.most_common(500) if c >= 1]
    for i, phrase in enumerate(candidates):
        secs_a = phrase_sec[phrase]
        for other in candidates[i + 1:]:
            secs_b = phrase_sec[other]
            if secs_a & secs_b:
                continue
            a, b = phrase.split(), other.split()
            if len(a) != len(b):
                continue
            diffs = [(x, y) for x, y in zip(a, b) if x != y]
            if len(diffs) != 1:
                continue
            x, y = diffs[0]
            if phrase_count[phrase] + phrase_count[other] < args.min_count:
                continue
            fx, fy = family_of(x), family_of(y)
            close = SequenceMatcher(None, x, y).ratio()
            if (fx is not None and fx == fy) or close > 0.82:
                report["synonym_pairs"].append({
                    "term_a": phrase, "sections_a": sorted(secs_a),
                    "term_b": other, "sections_b": sorted(secs_b),
                    "note": "these look like the same thing under two names — pick one and repeat it",
                })

    # dedupe symmetric pairs
    seen = set()
    unique = []
    for p in report["synonym_pairs"]:
        k = tuple(sorted([p["term_a"], p["term_b"]]))
        if k in seen:
            continue
        seen.add(k)
        unique.append(p)
    report["synonym_pairs"] = unique[:20]

    # ---- 2. explicit terms the author declared
    if args.terms:
        for t in [t.strip() for t in args.terms.split(",") if t.strip()]:
            present = [k for k in core_keys if re.search(re.escape(t), buckets[k], re.I)]
            absent = [k for k in core_keys if k not in present]
            report["term_coverage"].append({
                "term": t, "present_in": present, "absent_from": absent,
                "note": "defined term missing from %s — check whether a synonym crept in there"
                        % ", ".join(absent) if absent else "consistent across all sections",
            })

    # ---- 3. acronyms
    #
    # Module 3.7 asks for a definition in the abstract, in the main text, and in
    # each table and figure legend — because readers do not read linearly. It does
    # NOT ask for one per subsection: a paper with 25 subsections would then report
    # every acronym 20 times over, and the one real finding drowns in the list.
    #
    # So the checks are: never defined at all; used before it is defined; and
    # present in the abstract but defined only later. --strict restores the
    # per-section behaviour for anyone who wants it.
    first_def = {}          # acronym -> index in `order` of its first definition
    first_use = {}          # acronym -> index in `order` of its first use
    per_section = defaultdict(set)
    counts = Counter()
    for i, key in enumerate(order):
        text = buckets[key]
        for m in ACRONYM_RE.finditer(text):
            a = m.group(0)
            if (a in STANDARD or a.upper() in STANDARD or a in NOT_ACRONYMS
                    or a.isdigit() or len(a) > 8 or a in ("MATH",)):
                continue
            per_section[key].add(a)
            counts[a] += 1
            first_use.setdefault(a, i)
            window = text[max(0, m.start() - 100):m.end() + 100]
            defined = bool(re.search(r"\([^)]*\b" + re.escape(a) + r"\b[^)]*\)", window)) or \
                bool(re.search(re.escape(a) + r"\s*\([A-Za-z][^)]{3,}\)", window))
            if defined:
                first_def.setdefault(a, i)

    abstract_idx = order.index("abstract") if "abstract" in order else None
    for a in sorted(first_use, key=lambda x: (first_use[x], x)):
        where = [k for k in order if a in per_section[k]]
        if a not in first_def:
            report["acronyms"].append({
                "acronym": a, "section": ", ".join(where), "defined_in": None,
                "note": "never defined — spell it out (used %d times, in %s)"
                        % (counts[a], ", ".join(where)),
            })
        elif first_def[a] > first_use[a]:
            report["acronyms"].append({
                "acronym": a, "section": order[first_use[a]],
                "defined_in": order[first_def[a]],
                "note": "used in %s but not defined until %s"
                        % (order[first_use[a]], order[first_def[a]]),
            })
        elif (abstract_idx is not None and a in per_section["abstract"]
              and first_def[a] != abstract_idx):
            report["acronyms"].append({
                "acronym": a, "section": "abstract",
                "defined_in": order[first_def[a]],
                "note": "appears in the abstract but is defined in %s — the abstract "
                        "has to stand alone" % order[first_def[a]],
            })
        elif args.strict:
            for k in where:
                if k in CORE and k != order[first_def[a]]:
                    report["acronyms"].append({
                        "acronym": a, "section": k, "defined_in": order[first_def[a]],
                        "note": "defined only in %s; a reader starting at %s meets it cold"
                                % (order[first_def[a]], k),
                    })

    # Worth questioning whether they earn their keep at all.
    for a, n in sorted(counts.items(), key=lambda kv: kv[1]):
        if n <= 2 and a in first_def:
            report["acronyms"].append({
                "acronym": a, "section": order[first_use[a]], "defined_in": None,
                "note": "used only %d time%s — spelling it out costs less than the "
                        "abbreviation saves" % (n, "" if n == 1 else "s"),
            })

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print("=" * 78)
    print("KEYWORD CONSISTENCY — %s" % Path(args.path).name)
    print("=" * 78)
    print("Sections compared: %s\n" % ", ".join(core_keys))

    if report["synonym_pairs"]:
        print("-" * 78)
        print("SYNONYM DRIFT — the same thing under two names   (%d)" % len(report["synonym_pairs"]))
        print("-" * 78)
        for p in report["synonym_pairs"]:
            print("  «%s»  in %s" % (p["term_a"], ", ".join(p["sections_a"])))
            print("  «%s»  in %s" % (p["term_b"], ", ".join(p["sections_b"])))
            print("      %s\n" % p["note"])
    else:
        print("No synonym drift detected between sections.\n")

    if report["term_coverage"]:
        print("-" * 78)
        print("DECLARED TERMS")
        print("-" * 78)
        for t in report["term_coverage"]:
            mark = "ok " if not t["absent_from"] else "!! "
            print("  %s«%s»  %s" % (mark, t["term"], t["note"]))
        print()

    if report["acronyms"]:
        print("-" * 78)
        print("ACRONYMS ACROSS SECTIONS   (%d)" % len(report["acronyms"]))
        print("-" * 78)
        for a in report["acronyms"][:30]:
            print("  %-8s %s" % (a["acronym"], a["note"]))
        if len(report["acronyms"]) > 30:
            print("  … %d more" % (len(report["acronyms"]) - 30))
        print()

    print("=" * 78)
    print("Reminder: repeating a keyword is correct. Reaching for a thesaurus to avoid")
    print("repeating it is what creates this problem in the first place.")


if __name__ == "__main__":
    main()
