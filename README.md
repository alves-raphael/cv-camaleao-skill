# cv-camaleao

Skill do Claude Code que avalia a aderência de um currículo ao método **CV Camaleão** (PSP / Borderless Coding), pontua no checklist "CV Ready to Ship" (x/10) e gera uma versão corrigida em PDF single-column, ATS-friendly.

## Instalação

```bash
git clone git@github.com:alves-raphael/cv-camaleao-skill.git ~/.claude/skills/cv-camaleao
```

Ou, só para um projeto: clone em `<projeto>/.claude/skills/cv-camaleao`.

## Uso

No Claude Code, peça por exemplo: "avalie meu CV com o método Camaleão" e informe o PDF (e, opcionalmente, a vaga-alvo).

## Requisitos

`pdftotext`/`pdfinfo` (poppler-utils), Chrome ou Chromium, Python 3.

## Estrutura

- `SKILL.md`: fluxo de avaliação e reescrita
- `references/rubric.md`: checklist oficial de 10 itens e critérios por seção
- `references/rewrite.md`: STAR-M, Power Verbs, extração de métricas, customização por vaga
- `scripts/render_cv.py`: JSON → PDF (stdlib + Chrome headless)
- `examples/cv.example.json`: exemplo fictício do schema
