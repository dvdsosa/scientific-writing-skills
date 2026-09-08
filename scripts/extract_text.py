#!/usr/bin/env python3
"""Extract plain text and a section map from a manuscript.

Supports .tex, .docx, .md and .txt. The point is to let the sciwrite skills
work on the author's real files: without a section map, "review my Discussion"
forces the user to paste text by hand.

Usage:
    python extract_text.py paper.tex                 # section map + word counts
    python extract_text.py paper.tex --section disc  # print one section's text
    python extract_text.py paper.tex --json          # machine-readable

Section matching is fuzzy and case-insensitive: "disc", "Discussion",
"5" (index) all resolve. LaTeX extraction strips comments, math, figures,
tables and citation commands so the prose that comes out is what a reader
would actually read.
"""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

# Canonical IMRaD names, with the aliases journals and authors actually use.
CANONICAL = {
    "abstract": ["abstract", "summary", "resumen"],
    "introduction": ["introduction", "intro", "background", "introduccion", "introducción"],
    "methods": ["methods", "materials and methods", "method", "methodology",
                "materials", "experimental", "metodologia", "metodología", "materiales y metodos"],
    "results": ["results", "findings", "resultados"],
    "discussion": ["discussion", "discusion", "discusión"],
    "conclusion": ["conclusion", "conclusions", "concluding remarks", "conclusiones"],
    "limitations": ["limitations", "strengths and limitations", "limitaciones"],
    "related": ["related work", "state of the art", "literature review", "prior work"],
    "acknowledgements": ["acknowledgements", "acknowledgments", "agradecimientos"],
    "references": ["references", "bibliography", "referencias", "bibliografia", "bibliografía"],
}


def canonical_name(heading):
    h = heading.strip()
    # Leading numbering only when it is followed by a separator: "3.", "3.1 ", "IV.".
    h = re.sub(r"^\s*(?:\d+(?:\.\d+)*|[IVXLC]{1,6})\s*[.):]?\s+", "", h)
    h = h.lower()
    h = re.sub(r"[^a-záéíóúñü ]", "", h).strip()
    for canon, aliases in CANONICAL.items():
        for a in aliases:
            if h == a or h.startswith(a + " ") or h.endswith(" " + a):
                return canon
    return None


# --------------------------------------------------------------------------
# LaTeX
# --------------------------------------------------------------------------

# Environments whose content is not prose the author reads aloud.
DROP_ENVS = ["equation", "equation*", "align", "align*", "gather", "gather*",
             "eqnarray", "eqnarray*", "figure", "figure*", "table", "table*",
             "tabular", "tabularx", "lstlisting", "verbatim", "algorithm",
             "algorithmic", "tikzpicture", "thebibliography", "minted"]

# Commands whose *argument* is prose and should be kept.
KEEP_ARG = ["emph", "textit", "textbf", "texttt", "textsc", "text", "mbox",
            "underline", "footnote", "caption", "title"]

# Commands to delete entirely, argument included.
DROP_CMD = ["cite", "citep", "citet", "citeauthor", "citeyear", "autocite",
            "ref", "eqref", "autoref", "cref", "Cref", "pageref", "label",
            "includegraphics", "usepackage", "documentclass", "bibliography",
            "bibliographystyle", "input", "include", "newcommand",
            "renewcommand", "definecolor", "geometry", "hypersetup",
            "setlength", "vspace", "hspace", "index", "nocite"]


def strip_latex(src):
    # Comments (but keep escaped \%)
    src = re.sub(r"(?<!\\)%.*$", "", src, flags=re.M)

    # Everything before \begin{document} is preamble.
    m = re.search(r"\\begin\{document\}", src)
    if m:
        src = src[m.end():]
    src = re.split(r"\\end\{document\}", src)[0]

    # Drop non-prose environments wholesale.
    for env in DROP_ENVS:
        src = re.sub(r"\\begin\{" + re.escape(env) + r"\}.*?\\end\{" + re.escape(env) + r"\}",
                     " ", src, flags=re.S)

    # Display math is never prose.
    src = re.sub(r"\$\$.*?\$\$", " [equation] ", src, flags=re.S)
    src = re.sub(r"\\\[.*?\\\]", " [equation] ", src, flags=re.S)

    # Short inline math often carries the numbers a reader reads aloud
    # ("$n = 930$", "$12.4 \pm 1.03$"), and the consistency checks need them.
    def _inline(m):
        body = m.group(1)
        if len(body) > 40:
            return " [equation] "
        body = body.replace(r"\pm", "±").replace(r"\times", "×")
        body = body.replace(r"\%", "%").replace(r"\,", " ").replace("~", " ")
        body = re.sub(r"\\[a-zA-Z]+", " ", body)
        body = body.replace("{", "").replace("}", "").replace("^", "").replace("_", "")
        return " " + " ".join(body.split()) + " "

    src = re.sub(r"(?<!\\)\$([^$]*?)\$", _inline, src)

    # Two-argument commands where the first argument is formatting and the second
    # is prose: \textcolor{red}{...}, \colorbox{...}{...}. Keep the second only —
    # otherwise the colour name lands in the extracted text as a word.
    for cmd in ["textcolor", "colorbox", "fcolorbox", "hl"]:
        src = re.sub(r"\\" + cmd + r"\s*(?:\[[^\]]*\])?\s*\{[^{}]*\}\s*\{([^{}]*)\}",
                     r"\1", src)

    # Commands to remove with their argument. Longest first, so that \citep is
    # matched before \cite — otherwise \citep{key} leaves a stray "p key".
    for cmd in sorted(DROP_CMD, key=len, reverse=True):
        src = re.sub(r"\\" + cmd + r"\s*(\[[^\]]*\])?\s*(\{[^{}]*\})?", " ", src)

    # Commands whose argument is prose: unwrap.
    for _ in range(3):  # a few passes handle light nesting
        src = re.sub(r"\\(" + "|".join(KEEP_ARG) + r")\s*\{([^{}]*)\}", r"\2", src)

    # Any remaining single-argument command: unwrap the argument, drop the name.
    src = re.sub(r"\\[a-zA-Z@]+\s*(\[[^\]]*\])?\s*\{([^{}]*)\}", r"\2", src)
    # Bare commands and stray braces.
    src = re.sub(r"\\[a-zA-Z@]+\*?", " ", src)
    src = re.sub(r"\\[^a-zA-Z]", " ", src)
    src = src.replace("{", " ").replace("}", " ")
    src = re.sub(r"[ \t]+", " ", src)
    src = re.sub(r"\n\s*\n\s*\n+", "\n\n", src)
    return src.strip()


def _balanced(src, start):
    """Return the contents of a brace group whose opening brace is at start-1."""
    depth, out, i = 1, [], start
    while i < len(src):
        c = src[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return "".join(out)
        out.append(c)
        i += 1
    return "".join(out)


def sections_latex(src):
    """Split on \\section / \\subsection / \\chapter before stripping markup."""
    pattern = re.compile(r"\\(chapter|section|subsection|subsubsection)\*?\s*\{", re.M)
    out, pos = [], 0
    matches = list(pattern.finditer(src))
    if not matches:
        return [{"heading": "(document)", "level": 0, "canonical": None,
                 "text": strip_latex(src)}]

    # Text before the first heading. The abstract lives here, and journal classes
    # disagree about how to mark it: article uses the environment, MDPI/elsarticle
    # and friends use a \abstract{...} command.
    head = src[:matches[0].start()]
    ab = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", head, flags=re.S)
    abstract_text = ab.group(1) if ab else None
    if abstract_text is None:
        m_ab = re.search(r"\\abstract\s*\{", head)
        if m_ab:
            abstract_text = _balanced(head, m_ab.end())
    if abstract_text:
        out.append({"heading": "Abstract", "level": 1, "canonical": "abstract",
                    "text": strip_latex(abstract_text)})

    for i, m in enumerate(matches):
        # Balanced-brace read of the heading title.
        j, depth, title = m.end(), 1, []
        while j < len(src) and depth:
            c = src[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
            title.append(c)
            j += 1
        heading = strip_latex("".join(title)).strip() or "(untitled)"
        end = matches[i + 1].start() if i + 1 < len(matches) else len(src)
        level = {"chapter": 0, "section": 1, "subsection": 2, "subsubsection": 3}[m.group(1)]
        out.append({"heading": heading, "level": level,
                    "canonical": canonical_name(heading),
                    "text": strip_latex(src[j + 1:end])})
        pos = end
    return out


# --------------------------------------------------------------------------
# DOCX
# --------------------------------------------------------------------------

def sections_docx(path):
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    try:
        import xml.etree.ElementTree as ET
    except ImportError:  # pragma: no cover
        sys.exit("xml.etree unavailable")
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    out = [{"heading": "(document start)", "level": 0, "canonical": None, "text": ""}]
    for p in root.iter(ns + "p"):
        style = ""
        ppr = p.find(ns + "pPr")
        if ppr is not None:
            st = ppr.find(ns + "pStyle")
            if st is not None:
                style = st.get(ns + "val", "")
        text = "".join(t.text or "" for t in p.iter(ns + "t")).strip()
        if not text:
            continue
        m = re.match(r"Heading(\d)", style, re.I)
        if m:
            out.append({"heading": text, "level": int(m.group(1)),
                        "canonical": canonical_name(text), "text": ""})
        else:
            out[-1]["text"] += text + "\n\n"
    for s in out:
        s["text"] = s["text"].strip()
    return [s for s in out if s["text"] or s["heading"] != "(document start)"]


# --------------------------------------------------------------------------
# Markdown / plain text
# --------------------------------------------------------------------------

def sections_markdown(src):
    out = [{"heading": "(document start)", "level": 0, "canonical": None, "text": ""}]
    in_fence = False
    for line in src.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            title = m.group(2).strip()
            out.append({"heading": title, "level": len(m.group(1)),
                        "canonical": canonical_name(title), "text": ""})
        else:
            out[-1]["text"] += line + "\n"
    for s in out:
        s["text"] = s["text"].strip()
    return [s for s in out if s["text"] or s["heading"] != "(document start)"]


# --------------------------------------------------------------------------

def extract(path):
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return sections_docx(path)
    src = path.read_text(encoding="utf-8", errors="replace")
    if suffix == ".tex":
        return sections_latex(src)
    if suffix in (".md", ".markdown"):
        return sections_markdown(src)
    return [{"heading": "(document)", "level": 0, "canonical": None, "text": src.strip()}]


def words(text):
    return len(re.findall(r"\b[\w'-]+\b", text))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--section", help="print only this section (name, canonical name or index)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--full", action="store_true", help="print the whole extracted text")
    args = ap.parse_args()

    secs = extract(args.path)

    if args.full:
        print("\n\n".join(s["text"] for s in secs if s["text"]))
        return

    if args.section:
        q = args.section.strip().lower()
        if q.isdigit() and int(q) < len(secs):
            print(secs[int(q)]["text"])
            return
        for s in secs:
            if q in s["heading"].lower() or (s["canonical"] and q in s["canonical"]):
                print(s["text"])
                return
        sys.exit("No section matched %r. Available: %s"
                 % (args.section, ", ".join(s["heading"] for s in secs)))

    if args.json:
        print(json.dumps([{**s, "words": words(s["text"])} for s in secs],
                         ensure_ascii=False, indent=2))
        return

    total = sum(words(s["text"]) for s in secs)
    print("%s  —  %d sections, %d words of prose\n" % (Path(args.path).name, len(secs), total))
    for i, s in enumerate(secs):
        indent = "  " * s["level"]
        canon = "  [%s]" % s["canonical"] if s["canonical"] else ""
        print("%2d  %s%s%s" % (i, indent, s["heading"], canon))
        print("    %s%d words" % (indent, words(s["text"])))


if __name__ == "__main__":
    main()
