#!/usr/bin/env python3
"""Renderiza um CV Camaleão (JSON -> PDF single-column, ATS-friendly).

Uso: render_cv.py cv.json out.pdf [--check-only]

Python 3 puro (stdlib): sem Chrome, sem bibliotecas, sem fontes para instalar. O PDF usa as fontes
padrão do formato (Helvetica e Times), com texto real e links clicáveis, e sai igual em qualquer máquina.
Schema: ver ../examples/cv.example.json.
Imprime avisos objetivos (contagens, verbos proibidos, formato de data) e o número de páginas.
"""
import json
import re
import sys
import zlib
from pathlib import Path

SECTION_ORDER = ["Summary", "Key Achievements", "Experience", "Projects", "Skills", "Education & Certifications"]
BAD_STARTS = ("responsible for", "worked on", "worked with", "used ", "participated", "helped", "assisted", "involved in", "in charge of")
CLICHES = ("passionate", "eager to learn", "team player", "detail oriented", "detail-oriented", "fast learner", "seeking new challenges")
BR_DATE = re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b")
HAS_NUMBER = re.compile(r"\d")


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



# --- Métricas das fontes padrão do PDF (larguras por 1000 unidades, bytes cp1252 32..255) ---------
# Helvetica, Helvetica-Bold e Times-Bold existem em qualquer leitor de PDF, então nada é embutido.
HELV = [
    278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556,
    556, 556, 556, 556, 556, 556, 556, 278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667,
    611, 778, 722, 278, 500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667,
    667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500,
    222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584,
    750, 556, 500, 222, 556, 333, 1000, 556, 556, 333, 1000, 667, 333, 1000, 500, 611, 500, 500,
    222, 222, 333, 333, 350, 556, 1000, 333, 1000, 500, 333, 944, 500, 500, 667, 278, 333, 556, 556,
    556, 556, 260, 556, 333, 737, 370, 556, 584, 333, 737, 552, 400, 549, 333, 333, 333, 576, 537,
    333, 333, 333, 365, 556, 834, 834, 834, 611, 667, 667, 667, 667, 667, 667, 1000, 722, 667, 667,
    667, 667, 278, 278, 278, 278, 722, 722, 778, 778, 778, 778, 778, 584, 778, 722, 722, 722, 722,
    667, 667, 611, 556, 556, 556, 556, 556, 556, 889, 500, 556, 556, 556, 556, 278, 278, 278, 278,
    556, 556, 556, 556, 556, 556, 556, 549, 611, 556, 556, 556, 556, 500, 556, 500,
]
HELV_B = [
    278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556,
    556, 556, 556, 556, 556, 556, 556, 333, 333, 584, 584, 584, 611, 975, 722, 722, 722, 722, 667,
    611, 778, 722, 278, 556, 722, 611, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667,
    667, 611, 333, 278, 333, 584, 556, 333, 556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556,
    278, 889, 611, 611, 611, 611, 389, 556, 333, 611, 556, 778, 556, 556, 500, 389, 280, 389, 584,
    750, 556, 500, 278, 556, 500, 1000, 556, 556, 333, 1000, 667, 333, 1000, 500, 611, 500, 500,
    278, 278, 500, 500, 350, 556, 1000, 333, 1000, 556, 333, 944, 500, 500, 667, 278, 333, 556, 556,
    556, 556, 280, 556, 333, 737, 370, 556, 584, 333, 737, 552, 400, 549, 333, 333, 333, 576, 556,
    333, 333, 333, 365, 556, 834, 834, 834, 611, 722, 722, 722, 722, 722, 722, 1000, 722, 667, 667,
    667, 667, 278, 278, 278, 278, 722, 722, 778, 778, 778, 778, 778, 584, 778, 722, 722, 722, 722,
    667, 667, 611, 556, 556, 556, 556, 556, 556, 889, 556, 556, 556, 556, 556, 278, 278, 278, 278,
    611, 611, 611, 611, 611, 611, 611, 549, 611, 611, 611, 611, 611, 556, 611, 556,
]
TIMES_B = [
    250, 333, 555, 500, 500, 1000, 833, 278, 333, 333, 500, 570, 250, 333, 250, 278, 500, 500, 500,
    500, 500, 500, 500, 500, 500, 500, 333, 333, 570, 570, 570, 500, 930, 722, 667, 722, 722, 667,
    611, 778, 778, 389, 500, 778, 667, 944, 722, 778, 611, 778, 722, 556, 667, 722, 722, 1000, 722,
    722, 667, 333, 278, 333, 581, 500, 333, 500, 556, 444, 556, 444, 333, 500, 556, 278, 333, 556,
    278, 833, 556, 500, 556, 556, 444, 389, 333, 556, 500, 722, 500, 500, 444, 394, 220, 394, 520,
    778, 500, 500, 333, 500, 500, 1000, 500, 500, 333, 1000, 556, 333, 1000, 500, 667, 500, 500,
    333, 333, 500, 500, 350, 500, 1000, 333, 1000, 389, 333, 722, 500, 444, 722, 250, 333, 500, 500,
    500, 500, 220, 500, 333, 747, 300, 500, 570, 333, 747, 500, 400, 549, 300, 300, 333, 576, 540,
    333, 333, 300, 330, 500, 750, 750, 750, 500, 722, 722, 722, 722, 722, 722, 1000, 722, 667, 667,
    667, 667, 389, 389, 389, 389, 722, 722, 778, 778, 778, 778, 778, 570, 778, 722, 722, 722, 722,
    722, 611, 556, 500, 500, 500, 500, 500, 500, 722, 444, 444, 444, 444, 444, 278, 278, 278, 278,
    500, 556, 500, 500, 500, 500, 500, 549, 500, 556, 556, 556, 556, 500, 556, 500,
]

FONTS = {"F1": ("Helvetica", HELV), "F2": ("Helvetica-Bold", HELV_B), "F3": ("Times-Bold", TIMES_B)}
FALLBACK = {"→": "->", "←": "<-", "≥": ">=", "≤": "<=", "≈": "~", " ": " ", " ": " ", " ": " ", "✓": "", "✅": "", "‑": "-"}
LOSSY = set()
GRAY = 0.27


def clean(text):
    """Converte para caracteres que as fontes padrão (cp1252) sabem desenhar."""
    t = str(text or "")
    for a, b in FALLBACK.items():
        t = t.replace(a, b)
    out = []
    for ch in t:
        try:
            ch.encode("cp1252")
            out.append(ch)
        except UnicodeEncodeError:
            LOSSY.add(ch)
            out.append("?")
    return "".join(out)


def R(text, font="F1", size=10.0, color=0.0, url=None):
    """Um trecho de texto com estilo."""
    return (clean(text), font, size, color, url)


def sw(text, font, size):
    table = FONTS[font][1]
    return sum(table[b - 32] if 32 <= b < 256 else 500 for b in text.encode("cp1252")) * size / 1000


class Line:
    """Uma linha de layout. Ops: ("t", x, dy, texto, fonte, tamanho, cor, url) | ("r", x1, x2, dy, espessura)."""

    def __init__(self, h, base=0.0):
        self.h, self.base, self.ops = h, base, []


def spacer(h):
    return Line(h)


def wrap(runs, width):
    """Quebra runs em linhas -> [([(x_offset, token, largura)], largura_total)]."""
    toks, space = [], False
    for text, font, size, color, url in runs:
        for piece in re.findall(r"\s+|\S+", text):
            if piece.isspace():
                space = True
                continue
            toks.append((piece, font, size, color, url, space))
            space = False
    lines, cur, w = [], [], 0.0
    for t in toks:
        tw = sw(t[0], t[1], t[2])
        sp = sw(" ", t[1], t[2]) if (t[5] and cur) else 0.0
        if cur and w + sp + tw > width:
            lines.append((cur, w))
            cur, w, sp = [], 0.0, 0.0
        cur.append((w + sp, t, tw))
        w += sp + tw
    if cur:
        lines.append((cur, w))
    return lines or [([], 0.0)]


def text_lines(runs, x, width, align="left", lh_factor=1.32):
    size = max(r[2] for r in runs)
    lh = size * lh_factor
    base = (lh - size) / 2 + 0.9 * size
    out = []
    for toks, w in wrap(runs, width):
        ln = Line(lh, base)
        start = x if align == "left" else x + (width - w) / 2
        cur = None  # junta tokens vizinhos de mesmo estilo em um único Tj (extração de texto mais limpa)
        for dx, t, tw in toks:
            style = t[1:5]
            if cur and cur["style"] == style:
                cur["text"] += (" " if t[5] else "") + t[0]
            else:
                cur = {"x": start + dx, "text": t[0], "style": style}
                ln.ops.append(cur)
        ln.ops = [("t", o["x"], base, o["text"], *o["style"]) for o in ln.ops]
        out.append(ln)
    return out


def bullet(runs, x, width):
    ls = text_lines(runs, x + 14, width - 14)
    ls[0].ops.append(("t", x + 3, ls[0].base, clean("•"), "F1", 10.0, 0.0, None))
    return ls


def row(left, right, x, width):
    """Texto à esquerda e outro alinhado à direita na primeira linha."""
    ls = text_lines(left, x, width - (sw(right[0], right[1], right[2]) + 10 if right[0] else 0))
    if right[0]:
        ls[0].ops.append(("t", x + width - sw(right[0], right[1], right[2]), ls[0].base, *right))
    return ls


def heading(title, x, width):
    ln = text_lines([R(title, "F3", 12.5)], x, width, "center")[0]
    ln.h += 3
    ln.ops.append(("r", x, x + width, ln.h - 1.5, 0.6))
    return [spacer(8), ln, spacer(4)]


class Doc:
    def __init__(self, page):
        self.W, self.H = (612.0, 792.0) if str(page).lower() == "letter" else (595.28, 841.89)
        self.M, self.top, self.bottom = 42.0, self.H - 40, 40.0
        self.pages = [{"ops": [], "annots": []}]
        self.y = self.top

    @property
    def x(self):
        return self.M

    @property
    def width(self):
        return self.W - 2 * self.M

    def new_page(self):
        self.pages.append({"ops": [], "annots": []})
        self.y = self.top

    def place(self, lines):
        """Desenha as linhas juntas; se não couberem no resto da página, vai para a próxima."""
        total = sum(l.h for l in lines)
        if total > self.y - self.bottom and total <= self.top - self.bottom:
            self.new_page()
        for l in lines:
            if l.h > self.y - self.bottom:
                self.new_page()
            page = self.pages[-1]
            for op in l.ops:
                if op[0] == "t":
                    _, x, dy, text, font, size, color, url = op
                    page["ops"].append(("t", x, self.y - dy, text, font, size, color))
                    if url:
                        w = sw(text, font, size)
                        page["annots"].append((x, self.y - dy - 0.22 * size, x + w, self.y - dy + 0.8 * size, url))
                else:
                    _, x1, x2, dy, w = op
                    page["ops"].append(("r", x1, x2, self.y - dy, w))
            self.y -= l.h


def show_url(url):
    return re.sub(r"^https?://(www\.)?", "", url).rstrip("/")


def layout(cv):
    d = Doc(cv.get("page", "A4"))
    x, wd = d.x, d.width
    c = cv.get("contact", {})

    d.place(text_lines([R(cv["name"].upper(), "F3", 20)], x, wd, "center", 1.2))
    d.place(text_lines([R(cv["headline"], "F1", 11, GRAY)], x, wd, "center"))
    items = []
    if c.get("phone"):
        items.append(R(c["phone"]))
    if c.get("email"):
        items.append(R(c["email"], url="mailto:" + c["email"]))
    for l in c.get("links", []):
        items.append(R(l.get("label") or show_url(l["url"]), url=l["url"]))
    runs = []
    for i, it in enumerate(items):
        runs += ([R(" • ")] if i else []) + [it]
    if runs:
        d.place(text_lines(runs, x, wd, "center"))
    if c.get("location"):
        d.place(text_lines([R(c["location"])], x, wd, "center"))

    def section(title, chunks):
        chunks = [ch for ch in chunks if ch]
        if chunks:
            d.place(heading(title, x, wd) + chunks[0])
            for ch in chunks[1:]:
                d.place(ch)

    section("Summary", [text_lines([R(cv.get("summary"))], x, wd)])

    section("Key Achievements", [bullet([R(a["title"] + ":", "F2"), R(" " + a["text"])], x, wd) + [spacer(2)] for a in cv.get("achievements", [])])

    chunks = []
    for j in cv.get("experience", []):
        head = row([R(j["company"], "F2", 10.5)], R(j.get("location"), "F1", 10, GRAY), x, wd)
        head += row([R(j["role"])], R(j.get("period"), "F1", 10, GRAY), x, wd)
        if j.get("context"):
            head += text_lines([R(j["context"], "F2")], x, wd)
        bl = [bullet([R(b)], x, wd) for b in j.get("bullets", [])]
        parts = [head + (bl[0] if bl else [])] + bl[1:]
        parts[-1] = parts[-1] + [spacer(6)]  # mantém o cabeçalho junto do 1º bullet; o resto pode quebrar de página
        chunks += parts
    section("Experience", chunks)

    chunks = []
    for p in cv.get("projects", []):
        title = [R(p["name"], "F2")] + ([R(" — "), R(show_url(p["url"]), url=p["url"])] if p.get("url") else [])
        chunks.append(text_lines(title, x, wd) + text_lines([R(p["description"])], x, wd) + [spacer(5)])
    section("Projects", chunks)

    sk = []
    for g in cv.get("skills", []):
        sk += text_lines([R(g["group"] + ":", "F2"), R(" " + " · ".join(g["items"]))], x, wd) + [spacer(1.5)]
    section("Skills", [sk])

    chunks = [row([R(e["school"], "F2"), R(" — " + e["degree"])], R(e.get("period"), "F1", 10, GRAY), x, wd) + [spacer(2)] for e in cv.get("education", [])]
    if cv.get("certifications"):
        certs = " · ".join(z["name"] + (f" ({z['issuer']})" if z.get("issuer") else "") for z in cv["certifications"])
        chunks.append(text_lines([R("Certifications:", "F2"), R(" " + certs)], x, wd) + [spacer(2)])
    if cv.get("languages"):
        chunks.append(text_lines([R("Languages:", "F2"), R(" " + " · ".join(f"{l['name']} ({l['level']})" for l in cv["languages"]))], x, wd))
    section("Education & Certifications", chunks)
    return d


# --- Escrita do PDF ----------------------------------------------------------------------------
def pdf_str(text):
    return "".join(chr(b) if 32 <= b < 127 and chr(b) not in "()\\" else "\\%03o" % b for b in text.encode("cp1252"))


def content_stream(ops):
    out = []
    for op in ops:
        if op[0] == "t":
            _, x, y, text, font, size, color = op
            out.append(f"BT /{font} {size:.2f} Tf {color:.2f} g {x:.2f} {y:.2f} Td ({pdf_str(text)}) Tj ET")
        else:
            _, x1, x2, y, w = op
            out.append(f"0 G {w:.2f} w {x1:.2f} {y:.2f} m {x2:.2f} {y:.2f} l S")
    return "\n".join(out).encode("ascii")


def uri_str(url):
    return "".join(ch if 32 < ord(ch) < 127 and ch not in "()\\" else "\\%03o" % ord(ch) for ch in url.encode("utf-8").decode("latin-1"))


def build_pdf(doc, title):
    objs = [None, None]  # 1 = catálogo, 2 = árvore de páginas

    def add(data):
        objs.append(data)
        return len(objs)

    fonts = {k: add(f"<< /Type /Font /Subtype /Type1 /BaseFont /{base} /Encoding /WinAnsiEncoding >>".encode()) for k, (base, _) in FONTS.items()}
    info = add(("<< /Title <FEFF" + title.encode("utf-16-be").hex().upper() + "> /Producer (cv-camaleao) >>").encode())
    res = "<< /Font << " + " ".join(f"/{k} {i} 0 R" for k, i in fonts.items()) + " >> >>"
    page_ids = []
    for pg in doc.pages:
        data = zlib.compress(content_stream(pg["ops"]))
        cid = add(f"<< /Length {len(data)} /Filter /FlateDecode >>\nstream\n".encode("latin-1") + data + b"\nendstream")
        aids = [add(f"<< /Type /Annot /Subtype /Link /Rect [{a[0]:.2f} {a[1]:.2f} {a[2]:.2f} {a[3]:.2f}] /Border [0 0 0] /A << /S /URI /URI ({uri_str(a[4])}) >> >>".encode("latin-1")) for a in pg["annots"]]
        annots = f" /Annots [{' '.join(f'{i} 0 R' for i in aids)}]" if aids else ""
        page_ids.append(add(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {doc.W:.2f} {doc.H:.2f}] /Resources {res} /Contents {cid} 0 R{annots} >>".encode()))
    objs[0] = b"<< /Type /Catalog /Pages 2 0 R >>"
    objs[1] = f"<< /Type /Pages /Kids [{' '.join(f'{i} 0 R' for i in page_ids)}] /Count {len(page_ids)} >>".encode()

    out, offsets = bytearray(b"%PDF-1.4\n"), []
    for n, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{n} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    out += "".join(f"{o:010d} 00000 n \n" for o in offsets).encode()
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R /Info {info} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return bytes(out)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check_only = "--check-only" in sys.argv
    if not args or (len(args) < 2 and not check_only):
        sys.exit(__doc__)
    cv = json.loads(Path(args[0]).read_text(encoding="utf-8"))

    warnings = check(cv)
    doc = None if check_only else layout(cv)
    if doc:
        if len(doc.pages) > 2:
            warnings.append(f"{len(doc.pages)} páginas (máximo 2; corte conteúdo, não reduza a fonte)")
        if LOSSY:
            warnings.append("Caracteres sem suporte substituídos por '?': " + " ".join(sorted(LOSSY)))
    print("AVISOS:" if warnings else "Sem avisos objetivos.")
    for w in warnings:
        print(" -", w)
    if doc:
        out = Path(args[1]).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(build_pdf(doc, f"{cv['name']} — Resume"))
        print(f"PDF: {out} ({len(doc.pages)} páginas)")


if __name__ == "__main__":
    main()
