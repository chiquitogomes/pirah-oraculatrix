from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


agents = load("config/agent_registry.json")["agents"]
motors = load("config/motors.json")["motors"]
bases = load("config/bases.json")["bases"]
skills = load("config/skills.json")["skills"]
gates = load("config/gates.json")["gates"]
product_matrix = load("config/product_matrix.json")
scenarios = load("data/scenarios.json")
fusions = load("data/fusions.json")
summary = load("data/analysis_summary.json")


def esc(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def bullets(values: list[str]) -> str:
    return "; ".join(values)


def agent_registry_table() -> str:
    rows = [
        "| ID | Agente | Missão exclusiva | Por que independente | Inputs | Outputs | Paralelo | Memória | QA | Acionamento |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for a in agents:
        rows.append(
            f"| {a['id']} | {esc(a['name'])} | {esc(a['mission'])} | {esc(a['why_independent'])} | "
            f"{esc(bullets(a['inputs']))} | {esc(bullets(a['outputs']))} | {esc(a['parallelism'])} | "
            f"{esc(a['memory'])} | {esc(', '.join(a['qa_gates']))} | {esc(a['activation'])} |"
        )
    return "\n".join(rows)


def product_table() -> str:
    products = list(product_matrix)
    rows = ["| Agente | " + " | ".join(products) + " |", "|---|" + "---|" * len(products)]
    for a in agents:
        cells = ["●" if a["id"] in product_matrix[p] else "" for p in products]
        rows.append(f"| {a['id']} — {esc(a['name'])} | " + " | ".join(cells) + " |")
    return "\n".join(rows)


def motor_table() -> str:
    rows = ["| ID | Motor | Entrada | Saída | Técnica | Tolerância | QA |", "|---|---|---|---|---|---|---|"]
    for m in motors:
        rows.append(
            f"| {m['id']} | {esc(m['name'])} | {esc(m['input'])} | {esc(m['output'])} | "
            f"{esc(m['technique'])} | {esc(m['tolerance'])} | {esc(m['qa'])} |"
        )
    return "\n".join(rows)


def gate_table() -> str:
    rows = ["| Gate | Aprova quando | Bloqueia quando |", "|---|---|---|"]
    for g in gates:
        rows.append(f"| {g['id']} — {esc(g['name'])} | {esc(g['approve'])} | {esc(g['block'])} |")
    return "\n".join(rows)


def scenario_table() -> str:
    rows = ["| Cenário | Agentes | Motores | Bases | Skills | Gates | Custo relativo | Uso |", "|---|---:|---:|---:|---:|---:|---:|---|"]
    for s in scenarios:
        rows.append(
            f"| {s['scenario']} | {s['agents']} | {s['motors']} | {s['bases']} | {s['skills']} | "
            f"{s['gates']} | {s['relative_cost']:.1f}× | {s['use']} |"
        )
    return "\n".join(rows)


def blueprints() -> str:
    parts = [
        "# Blueprints dos 27 agentes — arquitetura provisória v1\n",
        "> Status: `DRAFT_ARCHITECTURE_V1`. Estes blueprints ainda dependem dos pilotos sintéticos A–H e não autorizam autoaprovação.\n",
    ]
    for a in agents:
        parts.extend(
            [
                f"## {a['id']} — {a['name']}\n",
                f"**Objetivo.** {a['mission']}\n",
                f"**Por que existe.** {a['why_independent']}\n",
                f"**Não faz.** {bullets(a['does_not'])}.\n",
                f"**Fontes.** {bullets(a['source_domains'])}.\n",
                f"**Ferramentas.** {bullets(a['tools'])}.\n",
                f"**Inputs.** {bullets(a['inputs'])}.\n",
                f"**Processo.** Opera apenas no escopo de `{a['activation']}`; registra versões, classes epistemológicas, claims, conflitos e incertezas.\n",
                f"**Outputs.** {bullets(a['outputs'])}.\n",
                f"**Agentes anteriores.** {', '.join(a['upstream']) or 'Nenhum obrigatório além do manifest de caso'}.\n",
                f"**Agentes posteriores.** {', '.join(a['downstream'])}.\n",
                f"**Paralelismo.** {a['parallelism']}\n",
                f"**Memória.** {a['memory']}\n",
                f"**Critérios de qualidade.** {bullets(a['quality_criteria'])}.\n",
                f"**Critérios de bloqueio.** {bullets(a['blockers'])}.\n",
                f"**Formato.** Seções: {', '.join(a['response_contract']['required_sections'])}; estados: {', '.join(a['response_contract']['statuses'])}.\n",
                f"**Prompt-base resumido.**\n\n> {a['prompt_base']}\n",
            ]
        )
    return "\n".join(parts)


REPORT = f"""# Arquitetura do Laboratório Astrológico, Hermético, Preditivo e Editorial Multiagente

## Resposta técnica

**O número ótimo recomendado é 27 agentes lógicos.** Eles são apoiados por **18 motores determinísticos**, **10 bases versionadas**, **16 skills compartilhadas** e **13 gates de QA**. A análise pontuou {summary['candidate_roles']} candidaturas, comparou {summary['pairwise_comparisons']} pares e documentou oito fusões. O conjunto ativo por produto fica entre {summary['active_agents_min']} e {summary['active_agents_max']} agentes; os 27 nunca devem ser acionados por reflexo.

Esse número não é uma declaração ontológica. É a menor arquitetura profissional encontrada nesta rodada que preserva: cálculo separado de interpretação; tradições segregadas; previsão separada de calibração; produção separada de auditoria; conteúdo separado de promessa comercial. Os motores não são “infalíveis”: devem ser **reprodutíveis, versionados, testados e fail-closed**.

O status correto é **arquitetura provisória v1**. O próprio comando-fonte proíbe congelar agentes definitivos antes da decomposição e das simulações. Nesta rodada foram usados seis auditores temporários; os 27 blueprints foram materializados, mas permanecem `DRAFT` até pilotos sintéticos A–H.

## Como o número emergiu

- Cerca de 120 atividades nomeadas foram consolidadas em 91 unidades funcionais.
- O filtro tipológico retirou cálculo, armazenamento, procedimento repetível e aprovação pura da disputa por “agente”.
- 35 papéis ultrapassaram o limiar indicativo de 38/50; a mediana foi {summary['score_median']:.0f}/50.
- O teste par-a-par avaliou função (50%), fontes (15%), ferramentas (15%) e outputs (20%).
- Oito fusões reduziram 35 candidaturas para 27 papéis lógicos, preservando modos internos e QA externo.
- Ausência de volume, SLA e orçamento impede decidir quantos processos permanentes devem ficar “quentes”; isso não impede definir a arquitetura lógica.

### Fusões governadas

| Candidaturas | Agente final | Condição de validade |
|---|---|---|
{chr(10).join(f"| {', '.join(item['from'])} | {item['to']} | {item['reason']} |" for item in fusions)}

## Organograma funcional

```mermaid
flowchart TD
    O["O01 · Direção e orquestração"] --> R["Pesquisa e evidências"]
    O --> A["Astrologia e previsão"]
    O --> H["Hermetismo, Tarot e materiais"]
    R --> S["Síntese especializada"]
    A --> S
    H --> S
    S --> E["Editorial, visual e mídia"]
    E --> Q["Q01–Q04 · QA independente"]
    Q --> X["Release ou devolução"]
```

Hierarquia operacional:

- Direção: O01.
- Pesquisa: R01–R02; verificação independente em Q02.
- Astrologia: A01–A09.
- Previsão: P01–P02.
- Hermetismo, Tarot e materiais: H01–H03, T01, N01.
- Editorial, visual, mídia e marketing: E01, V01, M01, M02.
- QA e release: Q01–Q04.

## Registro mestre dos agentes

{agent_registry_table()}

Os contratos completos, inclusive “não faz”, ferramentas, critérios de bloqueio, formato e prompt-base, estão no registro versionado e no caderno de blueprints.

## Motores determinísticos

{motor_table()}

Funções que **não** devem virar agentes: geocodificação, timezone/DST, efemérides, casas/aspectos, sorteio do Tarot, scoring, hashes, IDs, logs, renderização, transcodificação, analytics, formatação de citação, um agente por planeta/carta/casa/técnica/formato e qualquer agente nomeado por fornecedor.

## Bases e skills

### Bases

| ID | Base | Escopo |
|---|---|---|
{chr(10).join(f"| {b['id']} | {b['name']} | {b['scope']} |" for b in bases)}

### Skills compartilhadas

{chr(10).join(f"- {s['id']} — {s['name']}." for s in skills)}

## Matriz agente × produto

`●` significa acionamento-padrão; agentes adicionais só entram por risco, dúvida ou escopo.

{product_table()}

## Dependências, autoridade e impedimentos

| Camada | Alimenta | Revisada por | Nunca pode |
|---|---|---|---|
| Intake e motores | Especialistas | Q01 e Q03 | interpretar ou esconder ambiguidade |
| R01/R02 | Especialistas | Q02 | validar sozinhos a própria fonte |
| A01–A09, H01–H03, T01, N01 | P01/E01 | Q02/Q03 | aprovar o próprio claim |
| P01 | E01 | P02/Q03 | reescrever previsão após o evento |
| E01/V01/M01/M02 | Release candidate | Q04 | remover caveat ou autorizar promessa |
| Q01–Q04 | O01/release | autoridade humana em exceção crítica | produzir o artefato auditado |

Contratos obrigatórios: `CASE_MANIFEST`, `SOURCE_PACKET`, `CALCULATION_PACKET`, `CLAIM_PACKET`, `FORECAST_RECORD`, `REVIEW_PACKET`, `APPROVED_CONTENT_PACKET`, `RELEASE_CANDIDATE` e `RELEASE_MANIFEST`.

Identificadores mínimos: `TENANT_ID`, `CLIENT_ID`, `CASE_ID`, `PRODUCT_ID`, `RUN_ID`, `TASK_ID`, `ARTIFACT_ID`, `CLAIM_ID`, `CALCULATION_ID`, `SOURCE_ID`, `REVIEW_ID` e `RELEASE_ID`.

## Workflows

| Produto | Caminho | Paralelismo | Gargalo | Bloqueio típico |
|---|---|---|---|---|
| Mapa natal | intake → motores → A02/A03 → A01 → E01/V01 → QA | cálculo e pesquisa; A02/A03 | síntese sem colagem | hora/local ou método não resolvido |
| Previsão | freeze → A05/A06 → P01 → P02 → E01/V01 → QA | técnicas modernas/tradicionais | weighting e timing | look-ahead ou probabilidade não calibrada |
| Sinastria | consentimento duplo → mapas → A04 → E01/V01 → QA | dois mapas e cálculos relacionais | privacidade de terceiros | consentimento/dado assimétrico |
| Astrocartografia | ChartManifest → M11/M12 → A09 + pesquisa de lugares → V01 → QA | GIS e pesquisa local | hora natal e legibilidade | ranking preciso sem estabilidade |
| Hermético | R01 → H01/H02/H03/T01/N01 em cadernos separados → comparação → E01/V01 → QA | tradições em paralelo | conflitos de genealogia | harmonização ou tradução inadequada |
| Multimídia | claim freeze → E01 → brief M02 → V01/M01 → Q04 → publicação | ativos e formatos | deriva de conteúdo | promessa ou caveat removido |

### Simulações A–H

| Caso | Agentes principais | Passagens | Gargalo dominante | Riscos |
|---|---|---:|---|---|
| A · Natal | O01, R01, A01–A03, E01, V01, Q01–Q04 | 12–16 | síntese de escolas | hora, Barnum, excesso de fatores |
| B · Sinastria | O01, A01, A04, E01, V01, Q01–Q04 | 15–20 | consentimento e integração | determinismo afetivo e terceiro |
| C · Previsão anual | O01, A01, A05, A06, P01, P02, E01, V01, Q01–Q04 | 18–24 | convergência e weighting | cherry-picking e falsa precisão |
| D · Astrocartografia mundial | O01, A01, A09, P01, R02, E01, V01, Q01–Q04 | 18–26 | volume geográfico | timezone, mapa poluído, ranking instável |
| E · Eletiva | O01, A02, A07, P01, E01, Q01–Q03 | 10–15 | restrições × janelas | “eleição perfeita” e garantia |
| F · Evento histórico | O01, R01/R02, A02, A05/A06, A08, P02, E01, V01, Q01–Q04 | 22–32 | freeze factual | hindsight, causalidade e culpa |
| G · Hermético | O01, R01, H01–H03, T01, N01, E01, V01, Q02–Q04 | 18–28 | cadernos de tradição | sincretismo e citação apócrifa |
| H · Campanha multimídia | O01, E01, V01, M01, M02, Q02–Q04 | 14–22 | claim lock multiformato | sensacionalismo e inacessibilidade |

## Gates de qualidade

Cada gate emite somente `PASS`, `PASS_WITH_CAVEATS`, `RETURN_FOR_REVISION`, `BLOCKED` ou `HUMAN_DECISION_REQUIRED`.

{gate_table()}

Bloqueios de privacidade, contaminação entre clientes, integridade e segurança não admitem override automático. Uma exceção humana precisa de responsável, escopo, prazo, fundamento e registro imutável.

## Sistema de confiança

Não usar um score mágico. Exibir vetor:

- `C_input`: qualidade de data, hora, local e consentimento.
- `C_math`: reprodução matemática.
- `C_source`: adequação fonte × claim, não prestígio abstrato.
- `C_independence`: independência das fontes e revisão.
- `C_method`: aderência às regras declaradas.
- `C_tradition`: estabilidade genealógica e separação de tradições.
- `C_stability`: sensibilidade a hora, parâmetros e cenários.
- `C_convergence`: convergência pré-especificada.
- `C_calibration`: desempenho prospectivo fora da amostra.
- `C_interpretation`: estabilidade entre revisores.
- `C_privacy`: risco residual de identificação e acesso.
- `C_delivery`: equivalência editorial, visual, acessível e comercial.

Confiança preditiva só pode aparecer como probabilidade quando houver calibração prospectiva válida. Sem isso, usar classes qualitativas e a marca **não calibrada**. A nota pública, quando necessária, deve ser conservadora e limitada pelo pior eixo material.

## Modelo de fontes corrigido

A escala A–F do comando mistura tipo de evidência, autoridade e cálculo. O modelo recomendado usa duas dimensões:

1. Tipo de registro: input, cálculo, resultado empírico, fonte histórica primária, edição/tradução, pesquisa acadêmica, doutrina interna, manual profissional, prática contemporânea, relato ou hipótese.
2. Aptidão para o claim: autenticidade, proximidade, adequação, rigor editorial, transparência, reprodução, independência, corroboração, atualidade e localizador.

Fonte primária é forte para demonstrar o que um autor ensinava; não prova automaticamente antiguidade, eficácia ou genealogia. Cálculo não é fonte: precisa de inputs, algoritmo, versão, tolerância e `CALCULATION_ID`.

Os PDFs temáticos são **contêineres compostos**. A ingestão mínima deve ser obra + edição + página, preservando página do PDF e página impressa. O corpus atual é valioso, mas mistura história crítica, manuais populares, guidebooks, traduções automáticas e alegações modernas de saúde. Nenhuma obra ou claim foi publicado no Site; somente a arquitetura desidentificada.

## Arquiteturas alternativas

{scenario_table()}

### Essencial — 15

Serve a um piloto de baixo volume. Funde pesquisa, famílias astrológicas, Hermetismo/GD, Thelema/Tarot e parte editorial. É funcional, mas depende de prompts híbridos e contexto limpo para não permitir autoauditoria.

### Profissional recomendada — 27

É o ponto de equilíbrio. Mantém técnicas temporais moderna e tradicional separadas, três cadernos herméticos, quatro QAs independentes e uma cadeia editorial completa. O acionamento continua seletivo.

### Máxima eficiente — 42

Só se justifica após volume medido. Divide: psicológico × evolutivo; sinastria × composto/Davison; horária × eletiva; mundana × histórica; fatores especializados; Qabalah × GD; história do Tarot × leitura; Lenormand; ciência natural × correspondência; editor técnico × linguagem clara; arte × cartografia; audiovisual × gráfico/web; marca × mensuração; QA histórico × hermético. Acima de 42, o ganho marginal tende a ser menor que o custo de coordenação.

## Limitações e robustez

- Não foram fornecidos volume de clientes, frequência de produtos, SLA ou orçamento; os custos são relativos e provisórios.
- Os escores são julgamento especializado estruturado, não desempenho empírico dos agentes.
- O corpus PDF foi inventariado e amostrado; não houve ingestão integral obra a obra.
- A astrologia não possui validade preditiva científica estabelecida. O laboratório pode testar suas hipóteses, mas não apresentar o resultado como prova científica.
- O notebook está estruturalmente válido, mas o ambiente não possui Jupyter/nbformat para execução nativa; a mesma análise foi executada por `run_analysis.py` e seus totais foram validados.

## Próximos gates antes da instanciação definitiva

1. Criar datasets sintéticos para os casos A–H.
2. Rodar os 27 blueprints em modo simulado, com 8–14 agentes ativos por caso.
3. Medir retrabalho, taxa de devolução, tempo de fila, conflitos e custo por passagem.
4. Reexecutar a matriz de overlap com dados observados.
5. Testar isolamento de clientes e falhas fail-closed.
6. Submeter a revisão adversarial humana em privacidade, licenciamento da Swiss Ephemeris e promessas comerciais.
7. Somente então mudar o status de `DRAFT_ARCHITECTURE_V1` para uma versão operacional.
"""


DATA_CONTRACTS = """# Contratos de dados e passagem

## Envelope comum

Todo pacote deve conter: `schema_version`, `TENANT_ID`, `CLIENT_ID`, `CASE_ID`, `RUN_ID`, `TASK_ID`, produtor e versão, artefatos de entrada e hashes, método, ferramenta/modelo/configuração, classificação de dados, consumidores permitidos, claims, cálculos, fontes, incertezas, conflitos e status.

## CASE_MANIFEST

Identidade pseudonimizada; finalidade; consentimento; fonte de data/hora/local; calendário; precisão declarada; coordenadas e raio de incerteza; timezone e versão; candidatos UTC; JD-UT/JD-TT; Delta T; efeméride e hashes; zodíaco; casas; nodo; apogeu; orbes; catálogo estelar; flags; `CHART_HASH`.

## CLAIM_PACKET

`CLAIM_ID`; texto atômico; classe epistemológica; tradição; escopo; `SOURCE_IDs`; localizadores; `CALCULATION_IDs`; dependências; fontes contrárias; controvérsia; força documental; confiança interpretativa; incertezas; produtor; revisor; estado.

## FORECAST_RECORD

Alvo observável; população/caso; janela; horizonte; outcome; taxa de base; técnicas; pesos; redação exata; probabilidade ou classe; possibilidade de abstenção; `CONFIG_HASH`; timestamp anterior ao evento.

## REVIEW_PACKET

Checks; amostra; achados; severidade; reprodução; claims aprovados/devolvidos; bloqueios; correções; revisor independente; status.

## RELEASE_MANIFEST

Artefato, versão e hash; claims e caveats; fontes; direitos; Q01–Q04; audience/access; retenção; correções e retratações. Releases anteriores nunca são sobrescritos silenciosamente.
"""


README = """# Pirah Oraculatrix — laboratório multiagente

Arquitetura provisória e desidentificada de um laboratório de astrologia, Hermetismo, Tarot, pesquisa, previsão calibrada, edição e mídia.

## Decisão v1

- 27 agentes lógicos na arquitetura profissional recomendada.
- 18 motores determinísticos.
- 10 bases versionadas.
- 16 skills compartilhadas.
- 13 gates de QA.
- Status: `DRAFT_ARCHITECTURE_V1`.

## Conteúdo

- `config/agent_registry.json`: blueprints contratuais dos agentes.
- `config/motors.json`, `bases.json`, `skills.json`, `gates.json`: infraestrutura lógica.
- `data/candidate_scores.csv`: notas 0–5 das 35 candidaturas.
- `data/top_overlaps.csv`: auditoria par-a-par.
- `notebooks/architecture_scoring.ipynb`: notebook reprodutível; ver limitação de execução no relatório.
- `docs/architecture_report.md`: relatório técnico completo.
- `docs/agent_blueprints.md`: blueprints em formato legível.
- `docs/data_contracts.md`: contratos de handoff e proveniência.

Nenhum dado natal, documento pessoal ou conteúdo integral do corpus PDF faz parte deste repositório.
"""


(ROOT / "docs" / "architecture_report.md").write_text(REPORT, encoding="utf-8")
(ROOT / "docs" / "agent_blueprints.md").write_text(blueprints(), encoding="utf-8")
(ROOT / "docs" / "data_contracts.md").write_text(DATA_CONTRACTS, encoding="utf-8")
(ROOT / "README.md").write_text(README, encoding="utf-8")
print("generated", len(agents), "agent blueprints")
