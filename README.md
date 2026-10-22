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

Só **Python 3**. Nada mais para instalar.

- **Gerar o PDF:** `scripts/render_cv.py` usa apenas a biblioteca padrão. Escreve o PDF direto, com as fontes padrão do formato (Helvetica e Times), texto real, links clicáveis e o mesmo resultado em qualquer máquina. Não precisa de Chrome, de bibliotecas nem de fontes.
- **Ler o PDF a avaliar:** o Read do Claude Code lê PDF nativamente. `pdftotext`/`pdfinfo` (poppler) são opcionais.
- **Checar links:** usa `curl`, se existir. Sem ele, o item "links" fica como não verificado.

Limites conhecidos: o PDF gerado usa só caracteres do cp1252 (latim ocidental). Outros caracteres viram `?` e o script avisa. DOCX não é lido direto: exporte como PDF ou cole o texto.

Testado em Linux (Python 3.12). O gerador não usa nada específico de sistema operacional, mas macOS e Windows não foram testados.

## Estrutura

- `SKILL.md`: fluxo de avaliação e reescrita
- `references/rubric.md`: checklist oficial de 10 itens e critérios por seção
- `references/rewrite.md`: STAR-M, Power Verbs, extração de métricas, customização por vaga
- `scripts/render_cv.py`: JSON → PDF (Python puro)
- `examples/cv.example.json`: exemplo fictício do schema
