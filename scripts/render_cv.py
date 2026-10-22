#!/usr/bin/env python3
"""Renderiza um CV Camaleão (JSON -> PDF single-column, ATS-friendly).

Uso: render_cv.py cv.json out.pdf [--check-only]

Só usa a stdlib; o PDF é gerado pelo Chrome/Chromium headless.
Schema: ver ../examples/cv.example.json.
Imprime avisos objetivos (contagens, verbos proibidos, formato de data) e o número de páginas.
"""
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SECTION_ORDER = ["Summary", "Key Achievements", "Experience", "Projects", "Skills", "Education & Certifications"]
BAD_STARTS = ("responsible for", "worked on", "worked with", "used ", "participated", "helped", "assisted", "involved in", "in charge of")
CLICHES = ("passionate", "eager to learn", "team player", "detail oriented", "detail-oriented", "fast learner", "seeking new challenges")
BR_DATE = re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b")
HAS_NUMBER = re.compile(r"\d")


def esc(s):
    return html.escape(str(s or ""), quote=True)


def link(url, text=None):
    text = text or re.sub(r"^https?://(www\.)?", "", url).rstrip("/")
    return f'<a href="{esc(url)}">{esc(text)}</a>'


def check(cv):
    """Avisos objetivos. Não substitui a avaliação qualitativa."""
    w = []
    bullets = []
    exp = cv.get("experience", [])
    ach = cv.get("achievements", [])
    skills = cv.get("skills", [])
    n_skills = sum(len(g.get("items", [])) for g in skills)

    if len(ach) != 3:
        w.append(f"Key Achievements: {len(ach)} (deve ser exatamente 3)")
    for a in ach:
        if not HAS_NUMBER.search(a.get("text", "")):
            w.append(f"Achievement sem número: {a.get('title')}")
        bullets.append(a.get("text", ""))
    if skills and (len(skills) != 5 or not 20 <= n_skills <= 25):
        w.append(f"Skills: {len(skills)} blocos / {n_skills} skills (esperado 5 blocos / 20–25)")
    if not 3 <= len(exp) <= 4:
        w.append(f"Experience: {len(exp)} posições (esperado 3–4, salvo menos experiência disponível)")
    if not 2 <= len(cv.get("projects", [])) <= 4:
        w.append(f"Projects: {len(cv.get('projects', []))} (esperado 2–4)")
    if len(cv.get("summary", "").split()) < 40:
        w.append("Summary muito curto para 4 linhas densas")
    summary = cv.get("summary", "")
    if sum(len(re.findall(r"\d", s)) > 0 for s in re.split(r"(?<=[.!?])\s+", summary)) < 2:
        w.append("Summary: menos de 2 frases com métrica numérica")
    if re.search(r"\b(I|my|me)\b", summary, re.I):
        w.append("Summary em primeira pessoa (preferir impessoal)")

    verbs = []
    for job in exp:
        bs = job.get("bullets", [])
        if not 1 <= len(bs) <= 6:
            w.append(f"{job.get('company')}: {len(bs)} bullets (esperado 3–6; 1–2 só se experiência antiga)")
        for b in bs:
            bullets.append(b)
            verbs.append(b.split()[0].lower().strip(",") if b.split() else "")
            if not HAS_NUMBER.search(b):
                w.append(f"Bullet sem número: {b[:60]}…")
            if len(b) > 260:
                w.append(f"Bullet longo (>2 linhas?): {b[:60]}…")
    dup = sorted({v for v in verbs if verbs.count(v) > 1})
    if dup:
        w.append("Power Verb repetido: " + ", ".join(dup))

    alltext = " ".join(bullets + [summary])
    for b in bullets:
        if b.lower().startswith(BAD_STARTS):
            w.append(f"Bullet começa com verbo fraco: {b[:60]}…")
    for c in CLICHES:
        if c in alltext.lower():
            w.append(f"Clichê: '{c}'")
    dumped = json.dumps(cv, ensure_ascii=False)
    if BR_DATE.search(dumped):
        w.append("Data no formato DD/MM/AAAA (usar MM/YYYY)")
    if cv.get("photo"):
        w.append("Foto no CV (red flag fora de DE/FR)")
    if not re.search(r"GMT|UTC", cv.get("contact", {}).get("location", "")):
        w.append("Localização sem fuso horário (ex.: 'São Paulo, Brazil (GMT-3)')")
    return w


CSS = """
@page { size: %(page)s; margin: 14mm 15mm; }
* { box-sizing: border-box; }
body { font-family: Arial, 'Liberation Sans', Helvetica, sans-serif; font-size: 10pt; line-height: 1.32; color: #111; margin: 0; }
a { color: #111; text-decoration: none; }
h1 { font-family: 'Times New Roman', 'Liberation Serif', serif; font-size: 20pt; letter-spacing: .04em; text-transform: uppercase; text-align: center; margin: 0 0 2pt; }
.headline { text-align: center; color: #444; font-size: 11pt; margin: 0 0 3pt; }
.contact { text-align: center; font-size: 10pt; margin: 0 0 4pt; }
h2 { font-family: 'Times New Roman', 'Liberation Serif', serif; font-size: 12.5pt; text-align: center; margin: 11pt 0 5pt; padding-bottom: 2pt; border-bottom: 1px solid #111; break-after: avoid; }
p { margin: 0 0 3pt; }
ul { margin: 2pt 0 0 14pt; padding: 0; }
li { margin: 0 0 1.5pt; }
.row { display: flex; justify-content: space-between; gap: 8pt; }
.item { margin-bottom: 7pt; page-break-inside: avoid; }
.org { font-weight: bold; font-size: 10.5pt; }
.muted { color: #444; }
.ctx { font-weight: bold; margin: 1pt 0 1pt; }
.ach { margin-bottom: 3pt; }
.skills p { margin: 0 0 2pt; }
"""


def build_html(cv):
    c = cv.get("contact", {})
    parts = [c.get("phone"), c.get("email") and f'<a href="mailto:{esc(c["email"])}">{esc(c["email"])}</a>']
    parts += [link(l["url"], l.get("label")) for l in c.get("links", [])]
    contact = " &nbsp;•&nbsp; ".join(p if p and p.startswith("<a") else esc(p) for p in parts if p)
    contact += f'<br>{esc(c.get("location"))}'

    out = [f"<h1>{esc(cv['name'])}</h1>", f'<div class="headline">{esc(cv["headline"])}</div>', f'<div class="contact">{contact}</div>']

    out += ["<h2>Summary</h2>", f"<p>{esc(cv.get('summary'))}</p>"]

    out.append("<h2>Key Achievements</h2>")
    out.append("<ul>" + "".join(f'<li class="ach"><b>{esc(a["title"])}:</b> {esc(a["text"])}</li>' for a in cv.get("achievements", [])) + "</ul>")

    out.append("<h2>Experience</h2>")
    for j in cv.get("experience", []):
        out.append('<div class="item">')
        out.append(f'<div class="row"><span class="org">{esc(j["company"])}</span><span class="muted">{esc(j.get("location"))}</span></div>')
        out.append(f'<div class="row"><span>{esc(j["role"])}</span><span class="muted">{esc(j["period"])}</span></div>')
        if j.get("context"):
            out.append(f'<div class="ctx">{esc(j["context"])}</div>')
        out.append("<ul>" + "".join(f"<li>{esc(b)}</li>" for b in j.get("bullets", [])) + "</ul></div>")

    if cv.get("projects"):
        out.append("<h2>Projects</h2>")
        for p in cv["projects"]:
            out.append('<div class="item">')
            out.append(f'<div class="org">{esc(p["name"])}' + (f' <span class="muted">— {link(p["url"])}</span>' if p.get("url") else "") + "</div>")
            out.append(f'<p>{esc(p["description"])}</p></div>')

    if cv.get("skills"):
        out.append('<h2>Skills</h2><div class="skills">')
        out += [f'<p><b>{esc(g["group"])}:</b> {esc(" · ".join(g["items"]))}</p>' for g in cv["skills"]]
        out.append("</div>")

    out.append("<h2>Education &amp; Certifications</h2>")
    for e in cv.get("education", []):
        out.append(f'<div class="row"><span><b>{esc(e["school"])}</b> — {esc(e["degree"])}</span><span class="muted">{esc(e.get("period"))}</span></div>')
    if cv.get("certifications"):
        out.append("<p>" + " · ".join(f'{esc(x["name"])}' + (f' ({esc(x["issuer"])})' if x.get("issuer") else "") for x in cv["certifications"]) + "</p>")
    if cv.get("languages"):
        out.append("<p><b>Languages:</b> " + " · ".join(f'{esc(l["name"])} ({esc(l["level"])})' for l in cv["languages"]) + "</p>")

    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{esc(cv["name"])} — Resume</title><style>{CSS % {"page": cv.get("page", "A4")}}</style></head><body>{"".join(out)}</body></html>'


def chrome_bin():
    for b in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        if shutil.which(b):
            return b
    sys.exit("Chrome/Chromium não encontrado")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check_only = "--check-only" in sys.argv
    if not args or (len(args) < 2 and not check_only):
        sys.exit(__doc__)
    cv = json.loads(Path(args[0]).read_text(encoding="utf-8"))

    warnings = check(cv)
    print("AVISOS:" if warnings else "Sem avisos objetivos.")
    for w in warnings:
        print(" -", w)
    if check_only:
        return

    out = Path(args[1]).resolve()
    with tempfile.TemporaryDirectory() as d:
        page = Path(d) / "cv.html"
        page.write_text(build_html(cv), encoding="utf-8")
        subprocess.run([chrome_bin(), "--headless=new", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
                        f"--print-to-pdf={out}", page.as_uri()], check=True, capture_output=True)
    pages = re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(out)], capture_output=True, text=True).stdout)
    print(f"PDF: {out} ({pages.group(1) if pages else '?'} páginas)")


if __name__ == "__main__":
    main()
