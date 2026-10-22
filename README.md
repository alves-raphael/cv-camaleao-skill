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

| Para | Precisa de | Obrigatório |
|---|---|---|
| Gerar o PDF | Python 3 + **Chrome, Chromium ou Edge** | sim |
| Avaliar um PDF (extrair texto) | `pdftotext` (poppler) | não: sem ele, a skill usa a leitura de PDF do próprio Claude Code |
| Conferir páginas e fontes do PDF gerado | `pdfinfo`, `pdffonts` (poppler) | não: sem eles, o script conta as páginas sozinho e não confere as fontes |
| Fontes do layout | Arial / Times (macOS e Windows já têm); no Linux, `fonts-liberation` | recomendado: sem elas, o layout pode passar de 2 páginas |

Instalação do poppler: `apt install poppler-utils` · `brew install poppler` · Windows: via scoop/choco.

O script procura o navegador em `CHROME_BIN`, no PATH e nos caminhos padrão do macOS e do Windows. Se o seu estiver em outro lugar:

```bash
CHROME_BIN="/caminho/do/chrome" python3 scripts/render_cv.py cv.json cv.pdf
```

Chromium via snap: o script já tenta de novo gravando ao lado do destino. Se ainda falhar, use outro navegador via `CHROME_BIN`.

Testado apenas em Linux (Ubuntu, Chrome). macOS e Windows foram cobertos por caminho padrão, mas não testados.

## Estrutura

- `SKILL.md`: fluxo de avaliação e reescrita
- `references/rubric.md`: checklist oficial de 10 itens e critérios por seção
- `references/rewrite.md`: STAR-M, Power Verbs, extração de métricas, customização por vaga
- `scripts/render_cv.py`: JSON → PDF (stdlib + Chrome headless)
- `examples/cv.example.json`: exemplo fictício do schema
