from __future__ import annotations

import csv
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BRANCH_URL = "https://github.com/chiquitogomes/pirah-oraculatrix/blob/work/laboratorio-arquitetura-v1"


def load_json(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def load_csv(relative: str):
    with (ROOT / relative).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def sql_value(value):
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def values_sql(rows: list[dict], columns: list[str]) -> str:
    values = ",\n    ".join(
        "(" + ", ".join(sql_value(row.get(column)) for column in columns) + ")"
        for row in rows
    )
    return f"WITH source({', '.join(columns)}) AS (\n  VALUES\n    {values}\n)\nSELECT * FROM source;"


def execute_sql(sql: str) -> list[dict]:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    try:
        return [dict(row) for row in connection.execute(sql).fetchall()]
    finally:
        connection.close()


generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
registry = load_json("config/agent_registry.json")["agents"]
gates = load_json("config/gates.json")["gates"]
scenarios = load_json("data/scenarios.json")
fusions = load_json("data/fusions.json")
fusion_rows = [
    {"from": ", ".join(item["from"]), "to": item["to"], "reason": item["reason"]}
    for item in fusions
]
active_counts = load_csv("data/product_active_counts.csv")
candidate_scores = load_csv("data/candidate_scores.csv")

layer_by_prefix = {
    "O": "Direção", "R": "Pesquisa", "A": "Astrologia", "P": "Previsão",
    "H": "Hermetismo", "T": "Tarot", "N": "Materiais naturais",
    "E": "Editorial", "V": "Visual", "M": "Mídia e marketing", "Q": "QA",
}
agent_rows = [
    {
        "id": item["id"],
        "agent": item["name"],
        "layer": layer_by_prefix[item["id"][0]],
        "mission": item["mission"],
        "activation": item["activation"],
        "qa_count": len(item["qa_gates"]),
    }
    for item in registry
]
gate_rows = [
    {"id": item["id"], "gate": item["name"], "approve": item["approve"], "block": item["block"]}
    for item in gates
]
scenario_rows = [
    {
        "scenario": item["scenario"],
        "agents": item["agents"],
        "motors": item["motors"],
        "bases": item["bases"],
        "skills": item["skills"],
        "gates": item["gates"],
        "relative_cost": item["relative_cost"],
        "use": item["use"],
    }
    for item in scenarios
]
product_rows = [{"product": row["product"], "active_agents": int(row["active_agents"])} for row in active_counts]
score_rows = [
    {
        "candidate_id": row["candidate_id"],
        "candidate": row["candidate_name"],
        "score": int(row["total"]),
        "final_id": row["final_id"],
        "disposition": row["disposition"],
    }
    for row in candidate_scores
]
headline_sql = "SELECT 27 AS agents, 18 AS motors, 10 AS bases, 16 AS skills, 13 AS gates, 35 AS candidate_roles, 595 AS pairwise_comparisons;"
scenario_sql = values_sql(scenario_rows, ["scenario", "agents", "motors", "bases", "skills", "gates", "relative_cost", "use"])
agents_sql = values_sql(agent_rows, ["id", "agent", "layer", "mission", "activation", "qa_count"])
gates_sql = values_sql(gate_rows, ["id", "gate", "approve", "block"])
product_sql = values_sql(product_rows, ["product", "active_agents"])
scores_sql = values_sql(score_rows, ["candidate_id", "candidate", "score", "final_id", "disposition"])

headline_rows = execute_sql(headline_sql)
scenario_rows = execute_sql(scenario_sql)
agent_rows = execute_sql(agents_sql)
gate_rows = execute_sql(gates_sql)
product_rows = execute_sql(product_sql)
score_rows = execute_sql(scores_sql)

sources = [
    {
        "id": "src_report",
        "label": "Relatório técnico da arquitetura (GitHub, branch provisória)",
        "href": f"{BRANCH_URL}/docs/architecture_report.md",
        "query": {
            "language": "markdown",
            "description": "Síntese técnica derivada do comando mestre e das seis auditorias temporárias.",
            "tables_used": ["docs/architecture_report.md"],
            "executed_at": generated_at,
        },
    },
    {
        "id": "src_registry_doc",
        "label": "Registro contratual dos agentes e componentes",
        "href": f"{BRANCH_URL}/config/agent_registry.json",
        "query": {
            "language": "json",
            "description": "Registro provisório de agentes, motores, bases, skills, gates e matriz de produtos.",
            "tables_used": [
                "config/agent_registry.json", "config/motors.json", "config/bases.json",
                "config/skills.json", "config/gates.json", "config/product_matrix.json",
            ],
            "executed_at": generated_at,
        },
    },
    {
        "id": "src_command",
        "label": "Comando mestre anexado em 28 de agosto de 2026",
        "query": {
            "language": "markdown",
            "description": "Especificação arquitetural fornecida pelo usuário; arquivo privado não publicado.",
            "executed_at": generated_at,
        },
    },
    {
        "id": "src_headline",
        "label": "Contagens arquiteturais recomputadas",
        "href": f"{BRANCH_URL}/data/analysis_summary.json",
        "query": {"engine": "SQLite", "language": "sql", "sql": headline_sql, "description": "Contagens da arquitetura profissional e da auditoria.", "tables_used": ["literal_values"], "metric_definitions": ["agentes = papéis lógicos únicos no registro", "pares = n(n-1)/2 para n=35"], "executed_at": generated_at},
    },
    {
        "id": "src_scenarios",
        "label": "Três cenários arquiteturais",
        "href": f"{BRANCH_URL}/data/scenarios.json",
        "query": {"engine": "SQLite", "language": "sql", "sql": scenario_sql, "description": "Tabela limitada dos cenários essencial, profissional e máximo.", "tables_used": ["literal_values"], "executed_at": generated_at},
    },
    {
        "id": "src_agents",
        "label": "Registro dos 27 agentes",
        "href": f"{BRANCH_URL}/config/agent_registry.json",
        "query": {"engine": "SQLite", "language": "sql", "sql": agents_sql, "description": "Projeção auditável do registro de agentes.", "tables_used": ["literal_values"], "executed_at": generated_at},
    },
    {
        "id": "src_gates",
        "label": "Registro dos treze gates",
        "href": f"{BRANCH_URL}/config/gates.json",
        "query": {"engine": "SQLite", "language": "sql", "sql": gates_sql, "description": "Critérios de aprovação e bloqueio por gate.", "tables_used": ["literal_values"], "executed_at": generated_at},
    },
    {
        "id": "src_product",
        "label": "Carga de agentes por produto",
        "href": f"{BRANCH_URL}/data/product_active_counts.csv",
        "query": {"engine": "SQLite", "language": "sql", "sql": product_sql, "description": "Contagem dos agentes acionados por padrão em cada família de produto.", "tables_used": ["literal_values"], "metric_definitions": ["active_agents = número de IDs únicos na matriz agente × produto"], "executed_at": generated_at},
    },
    {
        "id": "src_scores",
        "label": "Escores das 35 candidaturas",
        "href": f"{BRANCH_URL}/data/candidate_scores.csv",
        "query": {"engine": "SQLite", "language": "sql", "sql": scores_sql, "description": "Escores e destino arquitetural das candidaturas.", "tables_used": ["literal_values"], "metric_definitions": ["score = soma de dez critérios de 0 a 5"], "executed_at": generated_at},
    },
]

artifact = {
    "surface": "report",
    "manifest": {
        "version": 1,
        "surface": "report",
        "title": "Arquitetura do Laboratório Oraculatrix",
        "description": "Auditoria técnica e blueprints provisórios do laboratório multiagente.",
        "generatedAt": generated_at,
        "sources": sources,
        "cards": [
            {"id": "card_agents", "dataset": "headline", "sourceId": "src_headline", "description": "Papéis lógicos da arquitetura profissional.", "metrics": [{"label": "Agentes", "field": "agents", "format": "number"}]},
            {"id": "card_motors", "dataset": "headline", "sourceId": "src_headline", "description": "Cálculos e serviços repetíveis.", "metrics": [{"label": "Motores", "field": "motors", "format": "number"}]},
            {"id": "card_bases", "dataset": "headline", "sourceId": "src_headline", "description": "Namespaces e registros versionados.", "metrics": [{"label": "Bases", "field": "bases", "format": "number"}]},
            {"id": "card_skills", "dataset": "headline", "sourceId": "src_headline", "description": "Capacidades compartilhadas entre agentes.", "metrics": [{"label": "Skills", "field": "skills", "format": "number"}]},
            {"id": "card_gates", "dataset": "headline", "sourceId": "src_headline", "description": "Checkpoints com poder de aprovar, devolver ou bloquear.", "metrics": [{"label": "Gates", "field": "gates", "format": "number"}]},
        ],
        "charts": [
            {
                "id": "chart_scenarios",
                "title": "Quantidade de agentes por cenário",
                "subtitle": "15 no piloto essencial, 27 no equilíbrio profissional e 42 no laboratório máximo",
                "intent": "comparison",
                "question": "Como a quantidade de agentes cresce entre os três níveis arquiteturais?",
                "rationale": "Barras permitem comparar três categorias discretas com zero explícito.",
                "type": "bar",
                "dataset": "scenarios",
                "sourceId": "src_scenarios",
                "encodings": {
                    "x": {"field": "scenario", "type": "nominal", "label": "Cenário"},
                    "y": {"field": "agents", "type": "quantitative", "label": "Agentes"},
                    "tooltip": [
                        {"field": "motors", "type": "quantitative", "label": "Motores"},
                        {"field": "gates", "type": "quantitative", "label": "Gates"},
                        {"field": "relative_cost", "type": "quantitative", "label": "Custo relativo"},
                    ],
                },
                "xAxisTitle": "Cenário",
                "yAxisTitle": "Agentes lógicos",
                "valueFormat": "number",
                "layout": "full",
                "maxRows": 3,
            },
            {
                "id": "chart_product_load",
                "title": "Agentes ativos por família de produto",
                "subtitle": "O acionamento seletivo evita mobilizar os 27 agentes em cada caso",
                "intent": "comparison",
                "question": "Quantos agentes são acionados por padrão em cada família de produto?",
                "rationale": "Barras com categorias discretas mostram a amplitude operacional sem sugerir tendência temporal.",
                "type": "bar",
                "dataset": "product_load",
                "sourceId": "src_product",
                "encodings": {
                    "x": {"field": "product", "type": "nominal", "label": "Produto"},
                    "y": {"field": "active_agents", "type": "quantitative", "label": "Agentes ativos"},
                },
                "xAxisTitle": "Família de produto",
                "yAxisTitle": "Agentes ativos",
                "valueFormat": "number",
                "layout": "full",
                "maxRows": 8,
            },
        ],
        "tables": [
            {
                "id": "table_agents",
                "title": "Registro dos 27 agentes",
                "subtitle": "Papéis lógicos da arquitetura profissional recomendada, em estado DRAFT",
                "dataset": "agents",
                "sourceId": "src_agents",
                "defaultSort": {"field": "id", "direction": "asc"},
                "density": "dense",
                "layout": "full",
                "columns": [
                    {"field": "id", "label": "ID", "type": "text"},
                    {"field": "agent", "label": "Agente", "type": "text"},
                    {"field": "layer", "label": "Camada", "type": "text"},
                    {"field": "mission", "label": "Missão", "type": "text"},
                    {"field": "activation", "label": "Acionamento", "type": "text"},
                ],
            },
            {
                "id": "table_gates",
                "title": "Gates de qualidade",
                "subtitle": "Treze checkpoints com critérios explícitos de aprovação e bloqueio",
                "dataset": "gates",
                "sourceId": "src_gates",
                "defaultSort": {"field": "id", "direction": "asc"},
                "density": "spacious",
                "layout": "full",
                "columns": [
                    {"field": "id", "label": "Gate", "type": "text"},
                    {"field": "gate", "label": "Nome", "type": "text"},
                    {"field": "approve", "label": "Aprova quando", "type": "text"},
                    {"field": "block", "label": "Bloqueia quando", "type": "text"},
                ],
            },
            {
                "id": "table_scores",
                "title": "Candidaturas e destino arquitetural",
                "subtitle": "35 papéis pontuados de 0 a 50 antes das fusões e reorganizações",
                "dataset": "candidate_scores",
                "sourceId": "src_scores",
                "defaultSort": {"field": "score", "direction": "desc"},
                "density": "dense",
                "layout": "full",
                "columns": [
                    {"field": "candidate_id", "label": "ID", "type": "text"},
                    {"field": "candidate", "label": "Candidatura", "type": "text"},
                    {"field": "score", "label": "Score", "type": "number"},
                    {"field": "final_id", "label": "Destino", "type": "text"},
                    {"field": "disposition", "label": "Decisão", "type": "text"},
                ],
            },
        ],
        "blocks": [
            {"id": "title", "type": "markdown", "body": "# Arquitetura do Laboratório Oraculatrix", "layout": "full"},
            {
                "id": "technical_summary",
                "type": "markdown",
                "sourceId": "src_report",
                "body": "## A menor arquitetura profissional contém 27 agentes lógicos\n\n**Resultado.** O núcleo recomendado combina 27 agentes, 18 motores, 10 bases, 16 skills e 13 gates. A equipe não é acionada inteira: cada produto mobiliza somente 7–14 agentes.\n\n**Decisão.** Os blueprints permanecem `DRAFT_ARCHITECTURE_V1`; seis auditores temporários foram usados para decompor e testar a arquitetura, mas nenhum agente definitivo foi congelado.\n\n**Limite.** Motores são reprodutíveis e fail-closed, não “infalíveis”; interpretação simbólica e previsão não se tornam fatos científicos.",
                "layout": "full",
            },
            {"id": "headline_metrics", "type": "metric-strip", "cardIds": ["card_agents", "card_motors", "card_bases", "card_skills", "card_gates"], "layout": "full"},
            {
                "id": "method_result",
                "type": "markdown",
                "sourceId": "src_scores",
                "body": "## O teste de 595 pares eliminou oito redundâncias\n\nTrinta e cinco candidaturas ultrapassaram o limiar indicativo de 38/50. A comparação par-a-par ponderou função, fontes, ferramentas e outputs. Oito fusões governadas reduziram o desenho para 27 papéis, sem fundir produção e auditoria nem Golden Dawn e Thelema. A mediana dos escores foi 46/50; esses números são julgamentos estruturados, não desempenho empírico.",
                "layout": "full",
            },
            {"id": "scenario_chart", "type": "chart", "chartId": "chart_scenarios", "layout": "full"},
            {
                "id": "scope_definition",
                "type": "markdown",
                "sourceId": "src_report",
                "body": "## Agente é julgamento; motor é cálculo; base é memória; gate é controle\n\nO filtro tipológico ocorre antes do score. Geocodificação, timezone, efemérides, casas, scoring, sorteio do Tarot, hashes, renderização e analytics não viram agentes. Bases armazenam conhecimento; skills reutilizam procedimentos; gates aprovam, devolvem ou bloqueiam. A confiança é um vetor — input, matemática, fontes, método, tradição, estabilidade, convergência, calibração, interpretação, privacidade e entrega — e nunca um único score mágico.",
                "layout": "full",
            },
            {
                "id": "agents_section",
                "type": "markdown",
                "sourceId": "src_registry_doc",
                "body": "## Os 27 agentes cobrem direção, pesquisa, astrologia, Hermetismo, Tarot, edição e QA\n\nCada blueprint define missão exclusiva, limites, inputs, outputs, fontes, ferramentas, memória, dependências, gates, blockers e prompt-base. O conjunto completo está na tabela e no registro contratual versionado.",
                "layout": "full",
            },
            {"id": "agents_table", "type": "table", "tableId": "table_agents", "layout": "full"},
            {
                "id": "selective_activation",
                "type": "markdown",
                "sourceId": "src_registry_doc",
                "body": "## O acionamento seletivo mantém a coordenação abaixo do custo de especialização\n\nCasos natais e relacionais usam o núcleo mais compacto; eventos históricos e previsões mobilizam mais revisores e especialistas. O gráfico mostra a carga-padrão por família, antes de escaladas por risco ou lacuna.",
                "layout": "full",
            },
            {"id": "product_chart", "type": "chart", "chartId": "chart_product_load", "layout": "full"},
            {
                "id": "gate_section",
                "type": "markdown",
                "sourceId": "src_registry_doc",
                "body": "## Treze gates impedem autoaprovação e mistura epistemológica\n\nQ01 recompõe cálculo; Q02 verifica evidências, astrologia e tradições; Q03 controla epistemologia, previsão, privacidade e segurança; Q04 libera a entrega editorial, visual e comercial. Privacidade, contaminação entre clientes e segurança não admitem override automático.",
                "layout": "full",
            },
            {"id": "gates_table", "type": "table", "tableId": "table_gates", "layout": "full"},
            {
                "id": "source_model",
                "type": "markdown",
                "sourceId": "src_command",
                "body": "## O corpus precisa ser atomizado por obra, edição e página\n\nOs PDFs são contêineres compostos, não bases homogêneas. O modelo rejeita uma hierarquia A–F linear e avalia tipo de registro e aptidão da fonte para cada claim. Fonte primária prova o que um autor afirmou; não prova automaticamente antiguidade, eficácia ou genealogia. Traduções automáticas, guidebooks e alegações modernas de saúde permanecem segregados. Nenhum conteúdo integral do corpus foi publicado.",
                "layout": "full",
            },
            {
                "id": "limitations",
                "type": "markdown",
                "sourceId": "src_report",
                "body": "## A recomendação é robusta como arquitetura, mas ainda não como operação\n\n**Limitações.** Não foram fornecidos volume, SLA, orçamento ou frequência dos produtos; o corpus foi inventariado e amostrado, não validado integralmente obra a obra; os escores são julgamento especializado; o notebook não pôde executar em Jupyter porque o ambiente não inclui Jupyter/nbformat, embora `run_analysis.py` tenha recomposto os totais.\n\n**Próximo gate.** Executar pilotos sintéticos A–H, medir retrabalho e taxa de devolução, testar isolamento e licenciamento, e só então promover os blueprints de `DRAFT` a operacionais.",
                "layout": "full",
            },
        ],
    },
    "snapshot": {
        "version": 1,
        "generatedAt": generated_at,
        "status": "ready",
        "datasets": {
            "headline": headline_rows,
            "scenarios": scenario_rows,
            "agents": agent_rows,
            "gates": gate_rows,
            "product_load": product_rows,
            "candidate_scores": score_rows,
            "fusions": fusion_rows,
        },
    },
    "sources": sources,
    "package_info": {
        "artifact_status": "DRAFT_ARCHITECTURE_V1",
        "snapshot_note": "Published snapshot; not a live connector.",
    },
}

(ROOT / "artifact.json").write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(generated_at)

