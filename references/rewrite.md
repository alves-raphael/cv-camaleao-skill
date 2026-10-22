# Guia de reescrita — CV Camaleão

## Regra zero: não fabricar

- Nunca invente empregador, cargo, datas, tecnologia, link, resultado ou número. O método permite **estimar com base em evidência real**, não inventar.
- Número que o candidato não confirmou: use `~` ou `approximately` (ex.: "~65%") **e** liste-o na seção "Confirmar com você" do relatório.
- Sem dado nenhum para um bullet: reescreva sem número e sinalize "faltou métrica", ou faça perguntas (seção "Extraindo métricas"). Não preencha com valor plausível.
- Preserve identidade e autoridade: muda a apresentação do valor, não o fato.

## Fórmula do bullet

`[Power Verb] + [S/T: contexto e tech] + [A: ação] + [R: resultado] + [M: magnitude]`

- Obrigatório: **Action + Result**; ideal: + **Magnitude**. 1–2 linhas, passado, tech dentro da frase.
- ❌ `Worked with Node.js and AWS to build backend services`
- ✅ `Facing a performance bottleneck in order processing, architected an event-driven scheduling service with Node.js, AWS EventBridge and Lambda, reducing dispatch errors by 73% while processing 100k+ daily events at 99.9% success rate`
- Padrões válidos: Tech + Result + Scale · Problem + Action + Impact · Context + Tech + Outcome.
- Alterne a ênfase (T vs. S) entre experiências e **não repita Power Verb** no CV.

## Power Verbs

| Categoria | Verbos |
|---|---|
| Construção | Architected, Engineered, Implemented, Developed, Built, Designed, Created, Established |
| Performance | Optimized, Accelerated, Streamlined, Enhanced, Improved, Reduced, Increased, Boosted |
| Liderança | Spearheaded, Drove, Championed, Led, Directed, Orchestrated, Coordinated, Pioneered |
| Resolução | Resolved, Eliminated, Debugged, Diagnosed, Mitigated, Fixed, Addressed, Troubleshot |
| Escala | Scaled, Migrated, Automated, Transformed, Refactored, Modernized, Consolidated |
| Análise | Analyzed, Evaluated, Assessed, Investigated, Researched, Identified, Defined |
| Colaboração | Collaborated, Partnered, Mentored, Facilitated, Integrated, Aligned, Contributed |
| Entrega | Deployed, Delivered, Launched, Released, Shipped, Rolled out, Executed |

Escolha: do zero → Architected/Engineered/Built · melhoria → Optimized/Enhanced/Improved · problema crítico → Resolved/Eliminated/Mitigated · crescimento → Scaled/Automated/Transformed.

Troca de tarefa por impacto: `Used MongoDB and Redis for data storage and caching` → `Optimized data access with MongoDB and Redis caching, [R] reducing … [M] serving …`.

## Extraindo métricas (quando o CV não tem números)

Pergunte ao candidato, de forma curta e em lote (no máximo 5–8 perguntas, só as dos bullets mais importantes):

1. **Antes/depois:** quanto tempo/custo/erros havia antes e depois? (deploy, build, query, tempo de resposta)
2. **Proxy:** quantos usuários/sessões/registros/requests por dia o sistema atendia? (banco, analytics, CloudWatch)
3. **Escala:** volume de eventos, mensagens, transações, uptime? (pergunte ao PM/PO, logs)
4. **Temporal:** bugs, incidentes, MTTR antes/depois de uma mudança? (Jira, Linear, Git history)
5. **Custo:** economia em cloud bill, infra, horas manuais.

Se o candidato só tiver estimativa, aceite com `~`.

## Header, Summary, Achievements

**Headline:** `<Cargo> | <Especialidade 1> | <Especialidade 2> | <Especialidade 3>`. Derive da vaga-alvo quando houver. Sem vaga: das 3 competências mais fortes e demonstradas.

**Summary (4 linhas):**
1. `<Cargo> with <N>+ years in <área>, specialized in <stack principal>.`
2. `<Métrica 1 com contexto>.`
3. `<Métrica 2 com contexto>.`
4. `Seeking <cargo/objetivo> in <tipo de time/empresa> to solve <desafio alinhado à vaga>.`
Impessoal, sem "I/My". Não repita nas linhas seguintes os anos/stack da linha 1.

**Key Achievements:** os 3 maiores resultados **mais relevantes para a vaga**, saídos do conjunto de achievements do Master. Título curto + 1 frase (Power Verb + feito + número + contexto).

## Experience

- Empresa | Cargo | Local (Remote, Country) | MM/YYYY – Present. Uma frase de contexto da empresa ("Largest virtual delivery support company in Brazil").
- 3–6 bullets, os mais relevantes à vaga primeiro. Cortar tarefas triviais (ex.: "used Git").
- Cargos compostos tipo "Solutions Architect & Backend Developer | DevOps & Cloud Specialist": só mantenha se sustentado pelos bullets e relevante.
- Experiências com 5+ anos: 1–2 bullets, ou bloco "Earlier Experience" no final da seção.
- Estágios/experiências muito antigas e irrelevantes: remover se faltar espaço.

## Skills

- 5 blocos, 20–25 skills. Escolha as que a vaga pede + as realmente sustentadas por experiência/projeto. Cada bloco com as skills da vaga no início.
- Sugestão de blocos: Languages & Frameworks · Cloud & DevOps · Databases & Messaging · Architecture & Testing · Tools & Observability (ou Soft Skills, se a vaga pedir).
- Remover duplicatas, sinônimos redundantes (React/ReactJS), nível de proficiência e skills sem evidência no CV.
- Com 5+ anos e sem espaço: omitir a seção (conta como cumprido) e investir o espaço em Experience/Projects.

## Projects

2–4 projetos com stack e **um resultado quantificado** (usuários, stars/downloads, performance). Link funcional obrigatório; sem link funcional, não listar. Prefira os de stack próxima à vaga.

## Customização Master → Enviado (quando houver vaga)

1. **Analise a vaga:** extraia 5–8 keywords/tecnologias principais, nível, país/região, desafios citados. Use a grafia **exata** da vaga (se pede "React.js", escreva "React.js").
2. **Mantenha:** header base, estrutura das 7 seções, educação, ordem cronológica, layout.
3. **Mude:** Summary (keywords + especialidades que a vaga busca, L4 alinhada), 3 Key Achievements (os mais relevantes), ordem e seleção de Skills, 2–3 Projects mais parecidos, cópia dos bullets para espelhar os desafios da vaga.
4. Distribua as keywords **de forma orgânica** (summary, bullets, skills), sem lista de keywords solta.
5. Ajuste ao país: fuso explícito, sem foto (US/UK), MM/YYYY.
6. Nunca adicione keyword de tecnologia que o candidato não usou. Se a vaga pede algo que ele não tem, diga isso no relatório como gap.

## Sem vaga-alvo

Gere o **CV Master**: mais completo, até 3–4 páginas permitido pela aula (mas nunca enviado). Avise que o arquivo para enviar é um CV Enviado, gerado por vaga, e ofereça gerá-lo. Se o usuário quer só um CV enviável sem vaga, produza a versão ≤ 2 páginas e deixe item 8 "não avaliável".
