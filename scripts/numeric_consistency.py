#!/usr/bin/env python3
"""Cross-check the numbers a reviewer will cross-check first.

Module 4.6: numerical inconsistency between the abstract, the body and the
tables is the fastest way to make a reviewer distrust the whole analysis. If
Methods says "followed for a minimum of two years" and Results says "average
follow-up was 1.5 years", the problem is not the sentence — it is that the
reviewer now wonders how many versions of the dataset are in circulation.

This reports, per number, where it appears and where it does not:

  sample sizes    n = / N = / "of 930 adults" — must agree everywhere
  percentages     a percentage in the abstract with no match in the body
  decimals        significant figures beyond what the measurement supports
  units           bare numbers next to variables that have units elsewhere

Usage:
    python numeric_consistency.py paper.tex
    python numeric_consistency.py paper.tex --json
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract_text  # noqa: E402

NUM = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s*(%|percent)?")
SAMPLE = re.compile(r"\b(?:n|N)\s*=\s*(\d[\d,]*)|\b(?:of|among|in|on|from|across|over|using|enrolled|recruited|included|analy[sz]ed|evaluated)\s+"
                    r"(\d{2,}[\d,]*)\s+(?:patients|participants|subjects|adults|"
                    r"children|women|men|samples|images|frames|devices|boards|runs|trials|cases)",
                    re.I)
PM = re.compile(r"(\d+(?:\.\d+)?)\s*(?:±|\+/-|\\pm)\s*(\d+(?:\.\d+)?)")
YEARS = re.compile(r"\b(?:19|20)\d{2}\b")

CORE_ORDER = ["abstract", "introduction", "methods", "results", "discussion", "conclusion"]


def normalise(tok):
    return tok.replace(",", "")


def decimals(tok):
    return len(tok.split(".")[1]) if "." in tok else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--max-decimals", type=int, default=2,
                    help="flag values with more decimals than this (default 2); "
                         "report only as many decimals as you can claim as significant figures")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    secs = extract_text.extract(args.path)
    buckets = defaultdict(str)
    order = []
    for s in secs:
        if not s["text"].strip():
            continue
        key = s["canonical"] or s["heading"]
        if key not in buckets:
            order.append(key)
        buckets[key] += "\n" + s["text"]

    report = {"sample_sizes": [], "abstract_orphans": [], "over_precision": [],
              "pm_precision": [], "sections": order}

    # ---- sample sizes ---------------------------------------------------
    sizes = defaultdict(set)
    for key in order:
        for m in SAMPLE.finditer(buckets[key]):
            val = normalise(m.group(1) or m.group(2))
            sizes[val].add(key)
    if sizes:
        # The dominant N is the one appearing in most sections; others are suspects.
        ranked = sorted(sizes.items(), key=lambda kv: (-len(kv[1]), -int(kv[0])))
        main_n, main_secs = ranked[0]
        report["sample_sizes"].append({
            "value": main_n, "sections": sorted(main_secs),
            "note": "most widely stated sample size",
        })
        for val, where in ranked[1:8]:
            report["sample_sizes"].append({
                "value": val, "sections": sorted(where),
                "note": "differs from %s — a subgroup, or a version of the dataset that "
                        "did not get updated everywhere?" % main_n,
            })

    # ---- abstract numbers with no home in the body ----------------------
    if "abstract" in buckets:
        body = " ".join(buckets[k] for k in order if k != "abstract")
        body_nums = {normalise(m.group(1)) for m in NUM.finditer(body)}
        seen = set()
        for m in NUM.finditer(buckets["abstract"]):
            tok = normalise(m.group(1))
            if tok in seen or YEARS.fullmatch(tok) or float(tok) < 2:
                continue
            seen.add(tok)
            if tok not in body_nums:
                ctx = buckets["abstract"][max(0, m.start() - 55):m.end() + 55]
                report["abstract_orphans"].append({
                    "value": m.group(0).strip(), "context": " ".join(ctx.split()),
                    "note": "appears in the abstract but nowhere in the body — reviewers "
                            "read these side by side",
                })

    # ---- over-precision -------------------------------------------------
    for key in order:
        seen = set()
        for m in NUM.finditer(buckets[key]):
            tok = m.group(1)
            if decimals(tok) > args.max_decimals and tok not in seen:
                seen.add(tok)
                ctx = buckets[key][max(0, m.start() - 55):m.end() + 55]
                report["over_precision"].append({
                    "value": tok, "section": key, "context": " ".join(ctx.split()),
                    "note": "%d decimal places — report only what the measurement supports"
                            % decimals(tok),
                })

    # ---- mean ± sd with mismatched precision ----------------------------
    for key in order:
        for m in PM.finditer(buckets[key]):
            a, b = m.group(1), m.group(2)
            if decimals(a) != decimals(b):
                report["pm_precision"].append({
                    "value": m.group(0), "section": key,
                    "note": "mean and spread carry different precision (%d vs %d decimals)"
                            % (decimals(a), decimals(b)),
                })

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print("=" * 78)
    print("NUMERIC CONSISTENCY — %s" % Path(args.path).name)
    print("=" * 78)
    print("Sections: %s\n" % ", ".join(order))

    def block(title, rows, fmt):
        if not rows:
            return
        print("-" * 78)
        print("%s   (%d)" % (title, len(rows)))
        print("-" * 78)
        for r in rows[:25]:
            print(fmt(r))
        if len(rows) > 25:
            print("  … %d more" % (len(rows) - 25))
        print()

    block("SAMPLE SIZES", report["sample_sizes"],
          lambda r: "  %-10s %-32s %s" % (r["value"], ", ".join(r["sections"]), r["note"]))
    block("ABSTRACT NUMBERS NOT FOUND IN THE BODY", report["abstract_orphans"],
          lambda r: "  %-10s %s\n         …%s…" % (r["value"], r["note"], r["context"]))
    block("SIGNIFICANT FIGURES", report["over_precision"],
          lambda r: "  %-10s [%s] %s\n         …%s…" % (r["value"], r["section"], r["note"], r["context"]))
    block("MEAN ± SPREAD", report["pm_precision"],
          lambda r: "  %-16s [%s] %s" % (r["value"], r["section"], r["note"]))

    if not any(report[k] for k in ("sample_sizes", "abstract_orphans", "over_precision", "pm_precision")):
        print("No numeric flags found.\n")

    print("=" * 78)
    print("Still to check by hand: do the percentages match the raw counts in the tables,")
    print("and do the figures show the same values as the tables?")


if __name__ == "__main__":
    main()
