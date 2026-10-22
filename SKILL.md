---
name: cv-camaleao
description: Avalia a aderência de um currículo ao método CV Camaleão (PSP / Borderless Coding), pontua no checklist "CV Ready to Ship" (x/10), aponta acertos e erros com correções concretas e gera uma nova versão em PDF single-column ATS-friendly. Use quando o usuário pedir para avaliar, revisar, pontuar, melhorar, reescrever ou criar um CV/currículo/resume, adaptar um CV a uma vaga (CV Master → CV Enviado) ou conferir se está "Ready to Ship".
---

# CV Camaleão — avaliar e reescrever

Referências (leia só o que precisar):
- `references/rubric.md` — checklist oficial de 10 itens, critérios por seção, red flags, severidade. **Leia sempre antes de avaliar.**
- `references/rewrite.md` — fórmula STAR-M, Power Verbs, como extrair métricas, customização por vaga. **Leia antes de reescrever.**
- `scripts/render_cv.py` + `examples/cv.example.json` — geram o PDF final a partir de JSON.

Responda ao usuário em **português**; o conteúdo do CV gerado fica em **inglês**.

## 1. Entrada

Aceite PDF, DOCX, Markdown ou texto colado (inclusive texto do LinkedIn). Opcional e muito valioso: **descrição da vaga-alvo**, anos de experiência e país/região.

- Sem vaga-alvo: avalie e gere o **CV Master**; item 8 do checklist fica "não avaliável". Ao final, ofereça gerar o CV Enviado se o usuário passar uma vaga.
- Não faça perguntas antes de avaliar. Avalie com o que tem; pergunte apenas ao chegar na reescrita (ver §4).

Extração de texto:
- PDF: `pdftotext -layout cv.pdf -` e `pdfinfo cv.pdf` (páginas). **Abra o PDF com Read** para ver o layout (colunas, fotos, gráficos, ícones). Texto sozinho não revela multi-coluna nem barras de proficiência.
- PDF sem texto extraível (só imagem) = bloqueante para ATS; avise.
- DOCX: `soffice --headless --convert-to pdf` e siga como PDF.

## 2. Avaliação

1. Pontue os 10 itens do `rubric.md`, **binários** (quase = 0). Para cada reprovado, cite a evidência exata do CV (trecho entre aspas).
2. Aplique os critérios por seção e liste red flags presentes.
3. Links: se houver rede, teste cada URL com `curl -sIL -o /dev/null -w "%{http_code} %{url_effective}\n" --max-time 10 <url>`. Código ≥ 400 ou falha = quebrado. Sem rede: "não verificado". LinkedIn costuma devolver 999/403 a bots: reporte "não verificável automaticamente, teste manualmente", não "quebrado".
4. Inglês: faça revisão, mas diga que é revisão por IA; item 9 só é garantido por nativo/Grammarly.
5. Nunca marque como aprovado o que não conseguiu verificar.

### Formato do relatório

```
# Avaliação CV Camaleão — <nome>
**Nota: X/10 — <veredito>**  (vaga-alvo: <sim/não>)

## Checklist
| # | Item | Status | Evidência / problema |
(10 linhas; ✅ ❌ ⚪ não verificado)

## O que está bom
- (curto, só o que realmente atende ao método)

## Problemas, por prioridade
### Bloqueantes
1. <seção> — "<trecho>" → por que viola → correção proposta (texto pronto)
### Importantes
### Polimento

## Red flags encontradas
## Gaps vs. a vaga (se houver): keywords/tecnologias que a vaga pede e o CV não sustenta
## Próximo passo: gerar versão corrigida? (+ perguntas necessárias)
```

Seja direto. Cada problema vem com a correção já escrita, não só o diagnóstico.

## 3. Referência de layout

`PSP-2026-GEAR-03-Template_CV.pdf` (na raiz do projeto) é a referência **visual**: nome centralizado, headline cinza, linha de contato, títulos de seção centralizados com filete, fontes serifada/sem serifa simples. O `render_cv.py` reproduz esse estilo.

**Não copie do template** o que viola as regras: Key Achievements em grade de 3 colunas, barras de proficiência em Languages, mais de 25 skills, bullets de tarefa sem métrica, Summary em primeira pessoa. Se o usuário citar o template como "o certo", avise dessas divergências; as regras do método (rubrica) prevalecem.

## 4. Reescrita (CV novo com todas as correções)

Gere somente se o usuário pedir ou aceitar a oferta do relatório.

1. Leia `references/rewrite.md`.
2. **Colete o que falta, em uma única rodada**: métricas dos bullets mais importantes (perguntas do rewrite.md), vaga-alvo se houver, links reais. Se o usuário preferir não responder, siga sem inventar: bullets sem número ficam marcados no relatório como pendência.
3. Monte um JSON no formato de `examples/cv.example.json` (salve em `./cv-camaleao/<nome>.json`). Regras duras:
   - **Nada de fatos inventados** (empresa, cargo, datas, tecnologia, link, número). Estimativas levam `~` e entram na lista "Confirmar com você".
   - Siga ordem e limites da rubrica (3 achievements, 3–4 experiências, 3–6 bullets, 5 blocos / 20–25 skills, 2–4 projetos, MM/YYYY, localização com fuso, sem foto).
   - Com vaga-alvo: aplique a customização Master → Enviado do rewrite.md.
4. Gere e confira:
   ```
   python3 -I <skill>/scripts/render_cv.py cv-camaleao/<nome>.json cv-camaleao/<nome>.pdf
   ```
   - Trate cada AVISO impresso (corrija o JSON e rode de novo até limpar, ou justifique por que é aceitável).
   - Páginas: ≤ 2 (1 se ≤ 5 anos de experiência e couber sem forçar). Se passar, corte o menos relevante, não diminua a fonte (< 10pt reprova).
   - Abra o PDF com Read e confira visualmente (coluna única, nada cortado). Rode `pdftotext -layout` e confirme que o texto sai em ordem de leitura.
5. Opcional: se o usuário quiser outro formato (DOCX, Markdown), derive do mesmo JSON.

## 5. Entrega final

Informe: caminho do PDF e do JSON; **nota após a correção, item a item**, separando:
- o que o PDF já cumpre;
- o que **depende do usuário** e impede o 10/10: links funcionando, números a confirmar, revisão de inglês por nativo, keywords sem vaga.

Só diga "Ready to Ship" se todos os 10 itens estiverem ✅ de fato. Caso contrário, diga quais faltam.
