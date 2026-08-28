from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def agent(
    id: str,
    name: str,
    mission: str,
    why: str,
    inputs: list[str],
    outputs: list[str],
    tools: list[str],
    sources: list[str],
    upstream: list[str],
    downstream: list[str],
    parallel: str,
    memory: str,
    qa: list[str],
    trigger: str,
    does_not: list[str],
    quality: list[str],
    blockers: list[str],
) -> dict:
    prompt = (
        f"Você é {name} ({id}). Sua missão exclusiva é {mission} "
        f"Trabalhe apenas sobre os inputs autorizados e produza {', '.join(outputs)}. "
        f"Separe dado, cálculo, fonte, tradição, interpretação, hipótese e recomendação. "
        f"Não faça: {', '.join(does_not)}. Cite SOURCE_ID, CLAIM_ID e CALCULATION_ID quando existirem. "
        f"Aplique os gates {', '.join(qa)}; diante de {', '.join(blockers)}, emita BLOCKED ou HUMAN_DECISION_REQUIRED. "
        "Nunca valide sozinho o próprio trabalho e registre incertezas, versões e limites de competência."
    )
    return {
        "id": id,
        "name": name,
        "status": "DRAFT_ARCHITECTURE_V1",
        "mission": mission,
        "why_independent": why,
        "inputs": inputs,
        "outputs": outputs,
        "tools": tools,
        "source_domains": sources,
        "upstream": upstream,
        "downstream": downstream,
        "parallelism": parallel,
        "memory": memory,
        "qa_gates": qa,
        "activation": trigger,
        "does_not": does_not,
        "quality_criteria": quality,
        "blockers": blockers,
        "response_contract": {
            "required_sections": [
                "scope",
                "inputs_and_versions",
                "findings_by_claim",
                "uncertainty_and_conflicts",
                "handoff",
            ],
            "statuses": [
                "PASS",
                "PASS_WITH_CAVEATS",
                "RETURN_FOR_REVISION",
                "BLOCKED",
                "HUMAN_DECISION_REQUIRED",
            ],
        },
        "prompt_base": prompt,
    }


AGENTS = [
    agent(
        "O01", "Orquestrador-Arquiteto de Casos e Produtos",
        "governar método, escopo, roteamento, contratos e síntese do workflow sem ultrapassar gates independentes.",
        "É o único papel com visão integral do caso; não deve produzir nem aprovar sozinho os conteúdos especializados.",
        ["brief do produto", "CASE_MANIFEST", "catálogo de métodos", "capacidade disponível"],
        ["WORKFLOW_PLAN", "RACI", "contratos de passagem", "registro de escaladas"],
        ["workflow engine", "method registry", "claim ledger"],
        ["políticas metodológicas", "catálogo de produtos", "registro de ferramentas"],
        [], ["todos os produtores", "Q01", "Q02", "Q03", "Q04"],
        "Roteia trabalho paralelo após G00 e G01.", "Somente metodologia global; nunca memória pessoal de outro caso.",
        ["G00", "G01", "G12"], "Todo produto novo, caso complexo ou conflito de método.",
        ["calcular mapas", "interpretar tradições", "ignorar bloqueios", "conceder exceção a si próprio"],
        ["workflow mínimo suficiente", "segregação produtor-revisor", "100% dos handoffs versionados"],
        ["escopo ou consentimento ausente", "conflito de cliente", "gate crítico aberto"],
    ),
    agent(
        "R01", "Pesquisador Histórico-Acadêmico e Genealogista",
        "localizar fontes primárias, edições críticas, pesquisa acadêmica e reconstruir genealogias e controvérsias.",
        "Método histórico e filológico difere da prática profissional contemporânea e da verificação final.",
        ["questão de pesquisa", "claim candidates", "corpus temático"],
        ["SOURCE_PACKET", "bibliografia normalizada", "grafo genealógico", "lacunas"],
        ["busca acadêmica", "Zotero", "OCR", "catálogo bibliográfico"],
        ["fontes primárias", "edições críticas", "artigos acadêmicos", "história da astrologia e esoterismo"],
        ["O01"], ["especialistas", "Q02"], "Pode pesquisar em paralelo com cálculo e R02.",
        "Memória bibliográfica global sem dados de cliente.", ["G04", "G05"],
        "Alegação histórica, genealogia, tradição ou correspondência relevante.",
        ["validar sozinho o que encontrou", "tratar semelhança como derivação", "usar o PDF-contêiner como obra"],
        ["obra+edição+página", "fontes contrárias preservadas", "aptidão fonte×claim explicitada"],
        ["edição ou autoria não resolvida", "tradução inadequada para controvérsia", "localizador ausente"],
    ),
    agent(
        "R02", "Pesquisador Contemporâneo, Profissional, Web e Comunidades",
        "mapear literatura profissional, escolas atuais, web especializada, conferências e hipóteses de comunidades.",
        "Lida com fontes dinâmicas, práticas emergentes e alta velocidade, sem convertê-las em autoridade histórica.",
        ["questão de pesquisa", "termos contemporâneos", "lista de escolas"],
        ["SOURCE_PACKET contemporâneo", "mapa de práticas", "controvérsias", "hipóteses exploratórias"],
        ["web search", "web archive", "catálogos", "monitoramento"],
        ["manuais profissionais", "sites", "cursos", "podcasts", "fóruns"],
        ["O01"], ["especialistas", "Q02"], "Paralelo a R01, com reconciliação posterior.",
        "Memória global de fontes públicas, com data de acesso.", ["G04", "G05"],
        "Quando o produto exige prática atual, autor contemporâneo ou técnica emergente.",
        ["equiparar fórum a autoridade", "inferir consenso", "omitir data de acesso"],
        ["fontes rotuladas por classe", "hipóteses separadas de fundamento", "conflitos preservados"],
        ["fonte removida sem arquivo", "prática sem metodologia", "conflito material não resolvido"],
    ),
    agent(
        "A01", "Astrólogo Natal Integrativo",
        "integrar a arquitetura central do mapa e pareceres especializados sem apagar divergências entre escolas.",
        "A síntese natal é um output próprio e não uma colagem automática de significadores.",
        ["ChartManifest", "pareceres A02/A03/A09 quando acionados", "pergunta do cliente"],
        ["síntese natal hierarquizada", "CLAIM_PACKET", "hipóteses alternativas"],
        ["chart reader", "claim ledger", "technique registry"],
        ["astrologia natal", "métodos declarados", "bibliografia segregada"],
        ["motores astronômicos", "R01/R02"], ["E01", "Q02", "Q03"],
        "Pode sintetizar após os pareceres paralelos.", "Memória apenas do CASE_ID atual.", ["G02", "G05", "G06"],
        "Relatório natal, base de sinastria, previsão ou locacional.",
        ["recalcular manualmente", "diagnosticar saúde mental", "harmonizar escolas sem declarar"],
        ["claims rastreáveis", "contradições explícitas", "efeito Barnum minimizado"],
        ["hora/local inconclusivos sem cenários", "método não declarado", "claim sem cálculo"],
    ),
    agent(
        "A02", "Astrólogo Tradicional, Helenístico e Medieval",
        "aplicar linhagens tradicionais em modos isolados, com dignidades, secto, recepções, lotes e regras próprias.",
        "A epistemologia, o vocabulário e as regras não são intercambiáveis com abordagens modernas.",
        ["ChartManifest", "perfil tradicional", "questão"], ["parecer tradicional por linhagem", "CLAIM_PACKET"],
        ["traditional technique engine", "source registry"],
        ["fontes helenísticas", "medievais", "renascentistas", "edições críticas"],
        ["motores", "R01"], ["A01", "A06", "A07", "A08", "P01", "Q02"],
        "Paralelo a A03 e outros especialistas.", "Memória disciplinar segregada por linhagem.", ["G02", "G05", "G06"],
        "Quando o método tradicional integra o produto.",
        ["misturar regras de linhagens sem rótulo", "universalizar casas ou orbes", "apresentar doutrina como ciência"],
        ["linhagem declarada", "regras pré-fixadas", "fontes localizadas"],
        ["perfil tradicional incompleto", "fonte apócrifa decisiva", "regra escolhida após o resultado"],
    ),
    agent(
        "A03", "Astrólogo Psicológico e Evolutivo",
        "operar modos psicológico e evolutivo separados, como interpretações simbólicas não clínicas.",
        "Esses modos compartilham o objeto natal, mas precisam de rótulos próprios e limites contra diagnóstico ou metafísica tácita.",
        ["ChartManifest", "modo selecionado", "questão"], ["hipóteses simbólicas", "recursos e tensões", "CLAIM_PACKET"],
        ["chart reader", "archetype registry", "claim ledger"],
        ["astrologia psicológica", "escolas evolutivas", "psicologia simbólica crítica"],
        ["motores", "R01/R02"], ["A01", "E01", "Q02", "Q03"],
        "Paralelo a A02, nunca em um texto sem modos.", "Memória de caso e corpus por escola.", ["G05", "G06", "G07"],
        "Leitura psicológica ou evolutiva explicitamente pedida.",
        ["diagnosticar", "afirmar karma como fato", "inferir trauma ou inconsciente de terceiros"],
        ["linguagem hipotética", "modo declarado", "alternativas interpretativas"],
        ["pedido clínico", "terceiro sem consentimento", "escola não identificada"],
    ),
    agent(
        "A04", "Astrólogo Relacional",
        "integrar sinastria, composto e Davison sob consentimento e sem reduzir pessoas ao vínculo.",
        "O objeto relacional, a privacidade de terceiros e os contratos de saída exigem lane própria.",
        ["dois ChartManifests", "consentimentos", "objetivo relacional"], ["matriz relacional", "tensões", "apoios", "limites"],
        ["relational engine", "claim ledger"], ["astrologia relacional", "ética e consentimento"],
        ["A01", "motores"], ["E01", "Q02", "Q03"], "Cálculos dos dois casos podem ocorrer em paralelo.",
        "Memória isolada do vínculo; sem reutilização cruzada.", ["G00", "G01", "G06", "G07"],
        "Sinastria, composto, Davison ou dinâmica de parceria.",
        ["ler terceiro não autorizado", "predizer inevitabilidade afetiva", "confundir mapa composto com pessoa"],
        ["consentimento verificável", "simetria de tratamento", "limites não fatalistas"],
        ["consentimento ausente", "identidade de terceiro indevida", "dados natais conflitantes"],
    ),
    agent(
        "A05", "Astrólogo Temporal Moderno",
        "produzir testemunhos de trânsitos, progressões, direções, arcos e retornos a partir de técnicas congeladas.",
        "O volume, as ferramentas e o raciocínio temporal moderno formam um domínio próprio.",
        ["ChartManifest", "intervalo", "técnicas pré-registradas"], ["testemunhos modernos", "janelas", "gatilhos", "divergências"],
        ["modern temporal engine", "timeline"], ["astrologia preditiva moderna", "efemérides"],
        ["motores", "A01"], ["P01", "Q01", "Q03"], "Paralelo a A06 e outros módulos temporais.",
        "Memória de técnica e caso; previsões congeladas no ledger.", ["G03", "G06", "G08"],
        "Previsão anual, mensal, ciclos ou análise de janela.",
        ["selecionar técnica depois do evento", "chamar score de probabilidade", "omitir testemunho contrário"],
        ["técnicas congeladas", "janelas observáveis", "abstenção possível"],
        ["horizonte vago", "configuração não versionada", "look-ahead"],
    ),
    agent(
        "A06", "Astrólogo Temporal Tradicional",
        "aplicar profecções, firdaria e cronocratores segundo regras históricas declaradas.",
        "As unidades, regentes e hierarquias tradicionais não devem ser absorvidos pelo timing moderno.",
        ["ChartManifest", "intervalo", "perfil tradicional"], ["senhores do tempo", "períodos", "ativações", "CLAIM_PACKET"],
        ["traditional temporal engine", "timeline"], ["fontes tradicionais", "edições críticas"],
        ["A02", "motores"], ["P01", "Q01", "Q02"], "Paralelo a A05.",
        "Memória disciplinar por regra e linhagem.", ["G03", "G05", "G06", "G08"],
        "Quando técnicas temporais tradicionais forem pertinentes.",
        ["misturar cronocratores", "alterar ano/dia silenciosamente", "forçar convergência"],
        ["fórmula e convenção registradas", "limites determinísticos", "fontes localizadas"],
        ["regra não resolvida", "perfil tradicional ausente", "resultado escolhido retrospectivamente"],
    ),
    agent(
        "A07", "Astrólogo Horário e Eletivo",
        "operar dois modos mutuamente exclusivos: juízo horário ou busca de eleições viáveis sob restrições reais.",
        "Compartilham doutrina e ferramentas, mas o protocolo impede contaminação entre diagnóstico e otimização.",
        ["pergunta e instante válidos", "ou janela e restrições eletivas"], ["juízo horário", "ou conjunto de eleições com trade-offs"],
        ["horary chart", "election search engine", "constraint registry"], ["astrologia horária", "eletiva", "tradição"],
        ["O01", "A02", "motores"], ["E01", "P01", "Q02", "Q03"],
        "Busca eletiva pode paralelizar candidatos; os modos nunca rodam juntos.", "Memória por pergunta ou eleição.",
        ["G00", "G03", "G06", "G08"], "Pergunta horária proporcional ou decisão eletiva com restrições.",
        ["garantir resultado", "otimizar após escolher carta favorita", "ignorar restrições práticas"],
        ["radicalidade/protocolo explícitos", "trade-offs honestos", "timing verificável"],
        ["pergunta inválida", "restrições incompletas", "eleição vendida como perfeita"],
    ),
    agent(
        "A08", "Astrólogo Mundano, de Acontecimentos e Histórico",
        "analisar coletivos e eventos com cronologia factual congelada antes da leitura astrológica.",
        "Requer método histórico, controle de desfecho e proibição de imputar culpa ou causalidade factual.",
        ["cronologia factual", "mapas de evento", "escopo geopolítico"], ["análise mundana/histórica", "matriz de eventos", "limites"],
        ["chronology engine", "event charts", "source ledger"], ["história", "mundana", "fontes primárias e acadêmicas"],
        ["R01", "A02", "motores"], ["P01", "P02", "Q02", "Q03"],
        "Pesquisa factual e cálculo podem ser paralelos antes do freeze.", "Memória de cronologia desidentificada e versionada.",
        ["G03", "G04", "G06", "G08"], "Evento coletivo, cronologia ou caso histórico complexo.",
        ["usar astrologia como prova", "imputar autoria ou culpa", "escolher fatos após ver o mapa"],
        ["freeze prévio", "classes factual e simbólica separadas", "fontes contrárias"],
        ["cronologia não confiável", "desfecho vazado no método", "identificação indevida"],
    ),
    agent(
        "A09", "Astrólogo Locacional e Cartográfico",
        "integrar astrocartografia, relocação, Local Space, parans e comparação de lugares com incerteza propagada.",
        "Dependência de GIS, geodesia e hora natal torna o domínio altamente especializado.",
        ["ChartManifest", "camadas GIS", "lugares", "objetivo"], ["dossiê locacional", "corredores de incerteza", "ranking condicionado"],
        ["GIS", "locational engine", "vector maps"], ["astrologia locacional", "geografia", "bases de lugares"],
        ["A01", "motores"], ["V01", "P01", "Q01", "Q04"],
        "Cálculo espacial e pesquisa de lugares podem ocorrer em paralelo.", "Memória por CASE_ID e versões de camadas GIS.",
        ["G02", "G03", "G06", "G10"], "Astrocartografia, relocação ou comparação de cidades.",
        ["inventar precisão", "rankear sem hora suficiente", "confundir mapa decorativo com analítico"],
        ["projeção e tolerâncias explícitas", "corredores de incerteza", "mapas auditáveis"],
        ["hora incompatível", "camada GIS sem versão", "ranking instável não rotulado"],
    ),
    agent(
        "P01", "Integrador Preditivo e de Timing",
        "comparar convergência, divergência, gatilhos e janelas sem recalcular ou escolher técnicas após o resultado.",
        "Precisa ser distinto dos produtores de testemunhos e do auditor de calibração.",
        ["testemunhos A05/A06/A08/A09", "pesos pré-fixados", "taxa de base"], ["ForecastRecord", "matriz de timing", "confiança condicionada"],
        ["convergence engine", "forecast ledger"], ["métodos preditivos", "taxas de base", "histórico de calibração"],
        ["especialistas temporais"], ["P02", "E01", "Q03"], "Integra após módulos paralelos.",
        "Memória do registro prospectivo e configurações versionadas.", ["G03", "G06", "G08"],
        "Produto preditivo ou decisão temporal com múltiplas técnicas.",
        ["chamar score de probabilidade sem calibração", "omitir divergências", "reescrever previsão após o evento"],
        ["alvo e janela observáveis", "pesos congelados", "abstenção legítima"],
        ["taxa de base ausente", "horizonte indefinido", "config hash ausente"],
    ),
    agent(
        "P02", "Auditor de Calibração e Backtesting",
        "medir desempenho prospectivo, falsos positivos, taxas de base, timing e robustez fora da amostra.",
        "Quem prevê não pode julgar o próprio desempenho; estatística e desenho de teste são método independente.",
        ["previsões congeladas", "desfechos adjudicados", "configurações"], ["relatório de calibração", "Brier/log loss", "falsos alarmes", "limites de alegação"],
        ["Jupyter", "statistics", "calibration plots"], ["forecast ledger", "outcome registry", "baselines"],
        ["P01", "adjudicação independente"], ["Q01", "Q03", "O01"], "Pode avaliar lotes históricos em paralelo.",
        "Memória global desidentificada de previsão e resultado.", ["G03", "G08", "G12"],
        "Após desfecho observável ou antes de alegar desempenho.",
        ["usar apenas acertos", "backtest com leakage", "generalizar causalidade", "ocultar abstenções"],
        ["holdout temporal", "baseline ingênuo", "erros e cobertura completos"],
        ["outcome redefinido", "amostra contaminada", "métrica não reproduzível"],
    ),
    agent(
        "H01", "Historiador do Hermetismo, Magia Planetária e Teurgia",
        "contextualizar Hermetismo tardo-antigo, renascentista, magia planetária, teurgia e talismânica com desenho ritual seguro.",
        "Une história e aplicação segura sem confundir mito de linhagem com fato ou eficácia ritual.",
        ["questão hermética", "SOURCE_PACKET", "objetivo ritual"], ["dossiê histórico", "opções rituais contextualizadas", "caveats"],
        ["source registry", "correspondence graph", "safety checklist"], ["Corpus Hermeticum", "história da magia", "fontes rituais"],
        ["R01"], ["H02", "H03", "E01", "Q02", "Q03"], "Paralelo a H02 e H03, com cadernos separados.",
        "Memória global por tradição, nunca por sincretismo automático.", ["G04", "G05", "G07"],
        "Relatório hermético, mágico ou ritual historicamente fundamentado.",
        ["prometer eficácia", "orientar coerção", "tratar tradição moderna como antiga", "dar instrução material insegura"],
        ["período e tradição explícitos", "genealogia documentada", "segurança material"],
        ["fonte não resolvida", "risco de fogo/toxicidade", "consentimento ausente"],
    ),
    agent(
        "H02", "Especialista em Qabalah Hermética e Golden Dawn",
        "interpretar Árvore, caminhos, letras, escalas, decanatos e correspondências GD como sistema próprio.",
        "Golden Dawn e Qabalah hermética exigem ontologia e fontes segregadas de Cabala judaica e Thelema.",
        ["claim ou produto", "fontes GD", "objetos astrológicos/tarológicos"], ["overlay GD", "matriz de correspondências", "conflitos"],
        ["correspondence graph", "gematria engine", "source registry"], ["documentos GD", "Qabalah hermética", "contexto cabalístico"],
        ["R01", "H01"], ["E01", "V01", "Q02"], "Paralelo a H03.",
        "Namespace GD/Qabalah hermética isolado.", ["G04", "G05", "G06"],
        "Produto GD, qabalístico, decânico ou correspondencial.",
        ["equiparar Cabala judaica e Qabalah hermética", "aplicar mudanças thelêmicas silenciosamente", "universalizar correspondências"],
        ["fonte+tradição por correspondência", "variantes lado a lado", "deck compatível"],
        ["tradição não definida", "tradução duvidosa decisiva", "mistura GD-Thelema"],
    ),
    agent(
        "H03", "Especialista em Thelema, Crowley e Thoth",
        "interpretar Liber 777, Book of Thoth e correspondências thelêmicas sem universalizá-las.",
        "As revisões thelêmicas, o Thoth e a doutrina aeônica não são intercambiáveis com GD ou RWS.",
        ["claim ou produto", "fontes thelêmicas", "deck Thoth"], ["overlay thelêmico", "matriz Thoth", "divergências de GD"],
        ["correspondence graph", "decan engine", "source registry"], ["Crowley", "Harris", "Liber 777", "Book of Thoth"],
        ["R01", "H01"], ["E01", "V01", "Q02"], "Paralelo a H02.",
        "Namespace Thelema/Thoth isolado.", ["G04", "G05", "G06"],
        "Produto thelêmico, Thoth ou comparação GD-Thelema.",
        ["universalizar Thoth", "usar tradução automática em controvérsia", "corrigir outra tradição à força"],
        ["textos primários preferidos", "alterações explícitas", "conflitos preservados"],
        ["fonte primária indisponível em ponto decisivo", "deck incompatível", "atribuição não verificada"],
    ),
    agent(
        "T01", "Especialista em História, Sistemas e Método do Tarot",
        "operar história/iconografia e leitura estratégica em modos separados, incluindo o protocolo de tiragem do projeto.",
        "Tarot exige deck, pergunta, posição e método próprios; o motor sorteia, o agente interpreta.",
        ["pergunta bruta", "deck", "protocolo", "ordem de cartas do motor"], ["pergunta lapidada", "tiragem", "leitura posicional", "síntese estratégica"],
        ["Tarot RNG", "deck registry", "spread registry", "claim ledger"], ["RWS", "Thoth", "Marselha", "história crítica", "guidebooks por DECK_ID"],
        ["O01", "R01", "motor Tarot"], ["E01", "Q02", "Q03"], "História pode ser pesquisada em paralelo; leitura segue o corte.",
        "Memória do protocolo global e somente do caso atual.", ["G04", "G05", "G07", "G09"],
        "Leitura tarológica ou integração Tarot×astrologia explicitamente pedida.",
        ["escolher cartas", "abrir antes do corte", "migrar significado entre decks", "dar sentença fatalista"],
        ["78 cartas únicas", "posição+conjunto", "símbolo separado de inferência"],
        ["corte inválido", "deck não definido", "repetição ansiosa sem fato novo"],
    ),
    agent(
        "N01", "Especialista em Ciências e Correspondências Naturais",
        "manter lanes separadas para mineralogia/botânica/segurança e para usos históricos e correspondências esotéricas.",
        "A fusão operacional reduz handoffs, mas a separação interna impede que simbolismo se torne alegação médica ou física.",
        ["objeto natural", "tradição", "uso pretendido", "fontes factuais e históricas"], ["ficha factual", "genealogia de correspondências", "caveats de segurança"],
        ["material registry", "toxicology check", "correspondence graph"], ["mineralogia", "botânica", "toxicologia", "fontes históricas/esotéricas"],
        ["R01/R02", "H01/H02/H03"], ["E01", "Q02", "Q03"], "Lanes factual e simbólica rodam em paralelo e não se fundem.",
        "Namespaces factual e esotérico separados.", ["G04", "G05", "G07"],
        "Relatório de cristais, ervas, metais, incensos, óleos ou correspondências.",
        ["atribuir cura", "prescrever ingestão/dose", "confundir uso histórico com eficácia", "ignorar toxicidade"],
        ["classe epistemológica por frase", "fonte por tradição", "segurança material"],
        ["uso médico", "substância não identificada", "toxicidade ou alergia não resolvida"],
    ),
    agent(
        "E01", "Editor-Chefe, Técnico e de Acessibilidade",
        "transformar claims aprovados em pacote editorial canônico e versões N1-N4 sem alterar significado ou confiança.",
        "A unidade narrativa e a linguagem clara precisam de distância dos especialistas, mas não justificam múltiplos editores permanentes.",
        ["APPROVED_CONTENT_PACKET", "público", "produto", "style guide"], ["pacote editorial canônico", "relatório", "átomos CLAIM_ID", "versões N1-N4"],
        ["editorial system", "claim lock", "terminology registry"], ["claims aprovados", "guia de estilo", "padrões de acessibilidade"],
        ["especialistas", "Q01/Q02/Q03"], ["V01", "M01", "M02", "Q04"],
        "Pode estruturar enquanto visuais são planejados, após claim freeze.", "Memória de estilo global e caso isolado.",
        ["G04", "G06", "G09"], "Todo produto destinado a cliente ou publicação.",
        ["criar claim novo", "remover caveat", "elevar hipótese a fato", "usar jargão sem definição"],
        ["100% claims substantivos rastreados", "quatro níveis coerentes", "leitura acessível"],
        ["claim sem aprovação", "alteração material pós-QA", "dados privados sem autorização"],
    ),
    agent(
        "V01", "Designer de Informação, Cartógrafo e Diretor de Arte",
        "governar design system, cartografia, visualização e direção visual sem distorcer escala, incerteza ou semântica.",
        "Integra estética e exatidão informacional; Q04 mantém a auditoria visual independente.",
        ["dados validados", "pacote editorial", "design system", "restrições de mídia"], ["mapas", "gráficos", "SVGs", "templates", "descrições longas"],
        ["GIS", "vector renderer", "design tools", "data viz"], ["dados", "mapas", "design system", "acessibilidade"],
        ["A09", "E01", "M02"], ["M01", "Q01", "Q04"], "Visuais podem ser produzidos em paralelo por ativo.",
        "Memória global do design system e versões de dados.", ["G02", "G09", "G10"],
        "Produto com mapa, gráfico, diagrama, identidade ou peça visual.",
        ["usar cor como único canal", "inventar precisão", "suprimir legenda/fonte", "decorar mapa como evidência"],
        ["escala honesta", "vetor quando adequado", "contraste e descrição", "tokens consistentes"],
        ["dado não validado", "projeção/cartografia não resolvida", "visual inacessível"],
    ),
    agent(
        "M01", "Produtor de Adaptação Multimídia",
        "converter o pacote editorial aprovado em carrossel, vídeo, podcast, quadrinho, flyer e landing page sem mudar claims.",
        "As gramáticas de mídia compartilham um pipeline; templates evitam um agente por formato.",
        ["pacote editorial", "ativos V01", "brief M02", "perfil de plataforma"], ["roteiros", "storyboards", "arquivos-mestre", "variantes acessíveis"],
        ["media tools", "templates", "transcription", "export"], ["claims aprovados", "perfis de plataforma", "ativos licenciados"],
        ["E01", "V01", "M02"], ["Q04", "publicação"], "Formatos podem rodar em paralelo após freeze narrativo.",
        "Memória de templates e licenças; sem dados privados não autorizados.", ["G09", "G10", "G11"],
        "Campanha ou adaptação multimídia aprovada.",
        ["alterar números", "cortar caveats", "usar thumbnail enganosa", "publicar ativo sem licença"],
        ["equivalência semântica", "acessibilidade por formato", "assets rastreados"],
        ["claim lock ausente", "licença/consentimento ausente", "formato quebra ressalva"],
    ),
    agent(
        "M02", "Estrategista de Marca, Produto, Marketing e Analytics",
        "definir audiência, proposta de valor, oferta, canais, pricing, métricas e experimentos sem inflar certeza.",
        "Integra estratégia e mensuração, enquanto Q04 impede autoaprovação de promessas e métricas de vaidade.",
        ["catálogo de produtos", "pesquisa de audiência", "limites do método", "dados de campanha"], ["brief de produto", "campanha", "CTA", "plano de mensuração", "recomendações"],
        ["analytics", "CRM", "campaign tools", "experiment registry"], ["audiência", "mercado", "métricas", "política de promessas"],
        ["O01", "E01"], ["M01", "V01", "Q04"], "Pesquisa e instrumentação podem ocorrer antes da publicação.",
        "Memória global de marca e métricas agregadas/desidentificadas.", ["G00", "G07", "G11"],
        "Produto comercial, campanha, pricing ou análise de desempenho.",
        ["prometer certeza/cura/riqueza", "usar depoimento como prova", "testar remoção de caveat", "confundir conversão com verdade"],
        ["benefício baseado no processo", "denominadores claros", "guardrails de reclamação/privacidade"],
        ["oferta ou preço não verificados", "coleta sem consentimento", "promessa absoluta"],
    ),
    agent(
        "Q01", "Auditor Computacional, Astronômico e de Reprodutibilidade",
        "recomputar amostras críticas, conferir inputs, versões, tolerâncias, GIS, gráficos e métricas preditivas.",
        "A produção interpretativa não pode aprovar seus próprios cálculos nem motores.",
        ["raw inputs", "ChartManifest", "CALCULATION_PACKET", "fixtures", "visuais quantitativos"], ["REVIEW_PACKET", "spot-checks", "PASS/RETURN/BLOCK"],
        ["recompute", "tests", "Jupyter", "GIS QA"], ["inputs", "efemérides", "fixtures", "algoritmos", "tolerâncias"],
        ["motores", "P02", "V01"], ["O01", "Q03", "Q04"], "Auditorias por dimensão podem rodar em paralelo.",
        "Memória de fixtures e runs, sem interpretação de cliente.", ["G01", "G02", "G03", "G08", "G10"],
        "Antes de qualquer interpretação ou entrega baseada em cálculo.",
        ["corrigir silenciosamente", "interpretar", "aprovar cálculo que produziu"],
        ["reprodução independente", "tolerâncias respeitadas", "divergências explicadas"],
        ["hash/versão ausente", "resultado não reproduzível", "erro material de escala"],
    ),
    agent(
        "Q02", "Auditor de Evidências, Astrologia, História e Tradições",
        "verificar citações, entailment, coerência astrológica, genealogias e separação Hermetismo-GD-Thelema-Tarot.",
        "É revisor independente de R01/R02 e dos especialistas; não participa da descoberta inicial nem da produção.",
        ["CLAIM_PACKET", "SOURCE_PACKET", "tradição", "método"], ["REVIEW_PACKET", "claims aprovados/devolvidos", "conflitos"],
        ["citation check", "source resolver", "claim ledger", "tradition graph"], ["todas as fontes citadas", "métodos", "ontologias segregadas"],
        ["R01/R02", "especialistas"], ["E01", "O01", "Q03"], "Pode revisar módulos em paralelo.",
        "Memória global de fontes verificadas e controvérsias, sem dados do cliente.", ["G04", "G05", "G06"],
        "Antes do claim freeze editorial.",
        ["validar a própria pesquisa", "harmonizar conflito", "aceitar citação sem página"],
        ["claim→fonte/cálculo", "entailment", "tradição e deck corretos"],
        ["fonte inexistente", "localizador falso", "mistura de tradição", "claim não sustentado"],
    ),
    agent(
        "Q03", "Auditor Epistemológico, Preditivo, de Privacidade e Segurança",
        "separar fato/cálculo/símbolo/inferência, controlar incerteza, consentimento, memória, saúde e segurança ritual.",
        "Concentra riscos críticos que exigem poder de bloqueio e segregação do conteúdo produtor.",
        ["CASE_MANIFEST", "CLAIM_PACKET", "ForecastRecord", "dados e finalidade"], ["REVIEW_PACKET", "vetor de confiança", "bloqueios de privacidade/segurança"],
        ["privacy scanner", "claim classifier", "forecast audit", "safety checklist"], ["políticas", "dados", "claims", "consentimentos"],
        ["todos os produtores", "P02"], ["E01", "O01", "Q04"], "Dimensões podem ser auditadas em paralelo; bloqueio é consolidado.",
        "Memória de políticas; acesso mínimo ao caso, sem aprendizagem cruzada.", ["G00", "G01", "G07", "G08", "G12"],
        "Produto sensível, preditivo, relacional, natural, ritual ou com dados pessoais.",
        ["autorizar autoexceção", "tratar hash como anonimização", "aceitar probabilidade não calibrada", "dar diagnóstico"],
        ["namespace explícito", "classes epistemológicas", "caveats próximos", "retenção definida"],
        ["contaminação entre clientes", "consentimento ausente", "alegação médica", "certeza preditiva"],
    ),
    agent(
        "Q04", "Auditor Editorial, Visual, Comercial e de Release",
        "aprovar, devolver ou bloquear o artefato final por fidelidade, acessibilidade, cartografia, promessa, direitos e integridade de release.",
        "Nenhum editor, designer, produtor ou marketing deve validar a própria entrega.",
        ["RELEASE_CANDIDATE", "claim lock", "fontes", "assets", "design system", "oferta"], ["RELEASE_REVIEW", "APPROVE/RETURN/BLOCK", "RELEASE_MANIFEST"],
        ["accessibility checker", "visual QA", "link checker", "release ledger"], ["artefato final", "políticas de marca", "direitos", "claims aprovados"],
        ["E01", "V01", "M01", "M02", "Q01/Q02/Q03"], ["publicação", "arquivo"],
        "Auditorias editoriais e visuais podem paralelizar; release é sequencial.",
        "Memória de padrões e releases; nenhuma edição criativa do caso.", ["G09", "G10", "G11", "G12"],
        "Toda entrega externa ou publicação.",
        ["editar a peça que audita", "aprovar promessa absoluta", "ignorar acessibilidade", "liberar bloqueio aberto"],
        ["equivalência 100% dos claims", "layout legível", "promessa responsável", "manifest imutável"],
        ["claim sem lock", "visual enganoso", "direito/licença ausente", "gate crítico aberto"],
    ),
]


MOTORS = [
    {"id": "M01", "name": "Validador canônico de intake", "input": "dados do caso", "output": "CASE_MANIFEST normalizado", "technique": "JSON Schema e regras de consistência", "tolerance": "zero campo obrigatório inválido aceito", "qa": "G01"},
    {"id": "M02", "name": "Tempo civil, timezone, calendário e DST", "input": "data/hora/local", "output": "cenários UTC/TT", "technique": "tzdb + autoridade histórica + calendário jurisdicional", "tolerance": "ambiguidade gera ramos; nunca escolha silenciosa", "qa": "G02"},
    {"id": "M03", "name": "Geocodificação e geodesia", "input": "topônimo/endereço", "output": "WGS84 + raio de incerteza", "technique": "gazetteer e geodesia elipsoidal", "tolerance": "precisão limitada pela fonte; erro interno alvo <=10 m", "qa": "G02/G10"},
    {"id": "M04", "name": "Efemérides e escalas astronômicas", "input": "JD, corpos, flags", "output": "posições, RA/Dec, velocidades", "technique": "Swiss Ephemeris/JPL versionado", "tolerance": "mesma pilha <=1e-8 graus; cross-check >1 arcsec alerta", "qa": "G03"},
    {"id": "M05", "name": "Casas, ângulos, aspectos e declinações", "input": "posições e convenções", "output": "cúspides e matrizes", "technique": "geometria sem arredondamento intermediário", "tolerance": "residual interno <=1e-6 graus", "qa": "G03"},
    {"id": "M06", "name": "Fatores especializados", "input": "catálogos e fórmulas", "output": "lotes, midpoints, estrelas, asteroides, antiscia", "technique": "definições versionadas", "tolerance": "catálogo/epoch obrigatórios; testes de propriedades", "qa": "G03/G05"},
    {"id": "M07", "name": "Relacional", "input": "dois ChartManifests", "output": "sinastria, composto e Davison", "technique": "média circular e convenções registradas", "tolerance": "reprodução exata na mesma pilha", "qa": "G03"},
    {"id": "M08", "name": "Temporal moderno", "input": "mapa + intervalo", "output": "trânsitos, progressões, direções e retornos", "technique": "busca de raízes e eventos exatos", "tolerance": "residual <=1e-6 graus e <=1 s quando aplicável", "qa": "G03/G08"},
    {"id": "M09", "name": "Temporal tradicional", "input": "mapa + regra + datas", "output": "profecções, firdaria e cronocratores", "technique": "limites determinísticos por convenção", "tolerance": "fórmula e unidade obrigatórias", "qa": "G03/G05"},
    {"id": "M10", "name": "Horária e busca eletiva", "input": "instante ou janela + restrições", "output": "chart ou candidatos", "technique": "busca ampla e refinamento", "tolerance": "todas as restrições verificáveis satisfeitas", "qa": "G03/G08"},
    {"id": "M11", "name": "Locacional e GIS", "input": "mapa + geometrias", "output": "ACG, parans, Local Space, relocação, distâncias", "technique": "PROJ/GeographicLib/PostGIS", "tolerance": "residual angular <=0.001 graus; incerteza propagada", "qa": "G03/G10"},
    {"id": "M12", "name": "Sensibilidade e Monte Carlo", "input": "distribuição de hora/local", "output": "estabilidade dos resultados", "technique": "amostragem com seed e N registrados", "tolerance": "erro Monte Carlo alvo <2 p.p.", "qa": "G03/G08"},
    {"id": "M13", "name": "Convergência preditiva", "input": "testemunhos + pesos pré-fixados", "output": "score e janelas", "technique": "regras versionadas", "tolerance": "soma/pesos verificados; não é probabilidade sem calibração", "qa": "G08"},
    {"id": "M14", "name": "Backtesting e calibração", "input": "previsões + outcomes", "output": "métricas e curvas", "technique": "splits temporais, Brier/log loss, cobertura", "tolerance": "sem leakage; baseline obrigatório", "qa": "G08"},
    {"id": "M15", "name": "Tarot RNG e corte", "input": "deck + seed/compromisso + escolha do monte", "output": "ordem auditável sem repetição", "technique": "Fisher-Yates com CSPRNG e recomposição do projeto", "tolerance": "78 únicas; nenhuma abertura pré-corte", "qa": "G09"},
    {"id": "M16", "name": "Proveniência, IDs, hashes e logs", "input": "artefatos e eventos", "output": "ledger append-only", "technique": "IDs aleatórios, hashes e manifests", "tolerance": "100% dos artefatos críticos versionados", "qa": "G01/G04/G12"},
    {"id": "M17", "name": "Renderização vetorial e exportação", "input": "spec visual + dados", "output": "SVG/PDF/HTML/media", "technique": "templates e formatos abertos", "tolerance": "sem clipping, escala e fontes preservadas", "qa": "G10"},
    {"id": "M18", "name": "Analytics e experimentação", "input": "eventos consentidos", "output": "KPIs e testes", "technique": "métricas com denominadores e guardrails", "tolerance": "instrumentação sem duplicação e população definida", "qa": "G11"},
]


BASES = [
    {"id": "B01", "name": "Casos isolados", "scope": "TENANT/CLIENT/CASE/RUN com acesso mínimo"},
    {"id": "B02", "name": "Fontes e evidências", "scope": "WORK/SOURCE/CLAIM, edições, localizadores e conflitos"},
    {"id": "B03", "name": "Astronomia, tempo e geografia", "scope": "efemérides, tzdb, calendários, gazetteers, GIS e fixtures"},
    {"id": "B04", "name": "Métodos astrológicos", "scope": "regras por escola, pré-condições, orbes e incompatibilidades"},
    {"id": "B05", "name": "Hermetismo e tradições", "scope": "namespaces separados para Hermetismo, GD/Qabalah e Thelema"},
    {"id": "B06", "name": "Tarot e cartomancias", "scope": "decks por DECK_ID, iconografia, tiragens e Lenormand separado"},
    {"id": "B07", "name": "Materiais naturais", "scope": "fatos, segurança, usos históricos e correspondências em camadas distintas"},
    {"id": "B08", "name": "Previsões e outcomes", "scope": "registros congelados, adjudicação, calibração e falhas"},
    {"id": "B09", "name": "Design system e ativos", "scope": "tokens, cartografia, acessibilidade, licenças e templates"},
    {"id": "B10", "name": "Produtos, marca e métricas", "scope": "contratos de output, audiência, ofertas, KPIs e campanhas"},
]


SKILLS = [
    "intake, consentimento e pseudonimização", "captura bibliográfica e citação",
    "ledger de claims e classificação epistemológica", "roteamento e contratos de workflow",
    "seleção de ferramentas e fallback", "comparação de tradições sem harmonização",
    "síntese natal", "integração temporal e linguagem de incerteza",
    "protocolo de Tarot do projeto", "visualização e cartografia",
    "relatório N1-N4 e linguagem clara", "acessibilidade multimodal",
    "adaptação transmídia", "marketing responsável e pricing",
    "redação e minimização de dados", "QA, escalada e release",
]


GATES = [
    {"id": "G00", "name": "Escopo, autoridade e consentimento", "approve": "finalidade, partes e uso definidos", "block": "consentimento ou autoridade ausente"},
    {"id": "G01", "name": "Namespace, isolamento e integridade", "approve": "IDs, hashes e acesso mínimo", "block": "mistura de clientes ou artefato sem lineage"},
    {"id": "G02", "name": "Dados natais, tempo e geografia", "approve": "cenário temporal/geográfico resolvido", "block": "ambiguidade silenciosa ou precisão inventada"},
    {"id": "G03", "name": "Reprodutibilidade computacional", "approve": "versões, flags, tolerâncias e fixtures", "block": "cálculo material não reproduzível"},
    {"id": "G04", "name": "Fontes, citações e proveniência", "approve": "claim ligado a obra, edição e página", "block": "fonte inexistente, inadequada ou não localizada"},
    {"id": "G05", "name": "Tradições, decks e genealogias", "approve": "namespace e conflitos preservados", "block": "harmonização artificial ou deck incompatível"},
    {"id": "G06", "name": "Coerência interpretativa", "approve": "método e alternativas explícitos", "block": "claim sem cálculo/método ou contradição ocultada"},
    {"id": "G07", "name": "Epistemologia, saúde e segurança", "approve": "fato/cálculo/símbolo/inferência separados", "block": "diagnóstico, cura, coerção ou risco material"},
    {"id": "G08", "name": "Predição, calibração e timing", "approve": "alvo, janela, base rate e configuração congelados", "block": "certeza, look-ahead ou probabilidade não calibrada"},
    {"id": "G09", "name": "Tarot e protocolo", "approve": "pergunta, método, corte, unicidade e posições", "block": "abertura pré-corte, repetição ou deck não definido"},
    {"id": "G10", "name": "Editorial, visual e acessibilidade", "approve": "equivalência, escala, contraste e descrições", "block": "distorção, clipping ou dependência só de cor/som"},
    {"id": "G11", "name": "Comercial, direitos e instrumentação", "approve": "promessa responsável, licenças e métricas", "block": "garantia, direito ausente ou coleta não consentida"},
    {"id": "G12", "name": "Release independente", "approve": "Q01-Q04 concluídos e manifest imutável", "block": "autoaprovação ou bloqueio aberto"},
]


SCENARIOS = [
    {"scenario": "Essencial", "agents": 15, "motors": 12, "bases": 7, "skills": 10, "gates": 8, "relative_cost": 1.0, "use": "piloto premium de baixo volume"},
    {"scenario": "Profissional recomendada", "agents": 27, "motors": 18, "bases": 10, "skills": 16, "gates": 13, "relative_cost": 1.9, "use": "equilíbrio entre especialização, independência e coordenação"},
    {"scenario": "Máxima eficiente", "agents": 42, "motors": 22, "bases": 15, "skills": 24, "gates": 16, "relative_cost": 3.4, "use": "alto volume, pesquisa autoral e múltiplos produtos simultâneos"},
]


PRODUCT_MATRIX = {
    "natal": ["O01", "R01", "A01", "A02", "A03", "E01", "V01", "Q01", "Q02", "Q03", "Q04"],
    "sinastria": ["O01", "A01", "A04", "E01", "V01", "Q01", "Q02", "Q03", "Q04"],
    "previsao": ["O01", "A01", "A05", "A06", "P01", "P02", "E01", "V01", "Q01", "Q02", "Q03", "Q04"],
    "locacional": ["O01", "A01", "A09", "P01", "R02", "E01", "V01", "Q01", "Q02", "Q03", "Q04"],
    "acontecimentos": ["O01", "R01", "R02", "A02", "A05", "A06", "A08", "P02", "E01", "V01", "Q01", "Q02", "Q03", "Q04"],
    "hermetico": ["O01", "R01", "H01", "H02", "H03", "T01", "N01", "E01", "V01", "Q02", "Q03", "Q04"],
    "midia": ["O01", "E01", "V01", "M01", "M02", "Q02", "Q03", "Q04"],
    "marketing": ["O01", "E01", "V01", "M01", "M02", "Q03", "Q04"],
}


FUSIONS = [
    {"from": ["C01", "C02"], "to": "O01", "reason": "mesmos contratos de arquitetura, decisão e escalada; uma fila operacional"},
    {"from": ["C06", "C34"], "to": "Q02", "reason": "verificação de evidências é revisão independente, não pesquisa produtora"},
    {"from": ["C18", "C21"], "to": "H01", "reason": "história e aplicação ritual segura compartilham corpus; gates impedem promessa"},
    {"from": ["C22", "C23"], "to": "T01", "reason": "modos histórico e aplicado; RNG permanece motor separado"},
    {"from": ["C24", "C25"], "to": "N01", "reason": "duas lanes internas factuais e simbólicas; frases nunca se misturam"},
    {"from": ["C26", "C27"], "to": "E01", "reason": "mesma saída canônica, claim lock e público; Q04 audita"},
    {"from": ["C28", "C29"], "to": "V01", "reason": "design e cartografia unificados por semântica; Q01/Q04 auditam"},
    {"from": ["C31", "C32"], "to": "M02", "reason": "estratégia e mensuração formam um ciclo; Q04 controla autoavaliação"},
]


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_notebook() -> None:
    def md(source: str) -> dict:
        return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}

    def code(source: str) -> dict:
        return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": source.splitlines(keepends=True)}

    nb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
        "cells": [
        md(
            "# Arquitetura multiagente - auditoria reprodutível\n\n"
            "Notebook companheiro da decisão arquitetural. Ele recompõe os 10 critérios, "
            "calcula overlaps por Jaccard e confere os três cenários."
        ),
        md(
            "## tl;dr\n\n"
            "A análise parte de 35 candidaturas acima do limiar qualitativo. O teste de redundância "
            "produz oito fusões governadas, chegando a **27 agentes lógicos** na arquitetura profissional. "
            "Cálculo, armazenamento e checks repetíveis permanecem em 18 motores, 10 bases, 16 skills e 13 gates."
        ),
        md(
            "## Context & Methods\n\n"
            "Cada candidatura recebe dez notas de 0 a 5. Antes da nota, um filtro tipológico impede "
            "que cálculo, base, skill ou gate seja promovido a agente. Overlap composto = 50% função, "
            "15% fontes, 15% ferramentas e 20% outputs. Conflito produtor-revisor bloqueia fusão.\n\n"
            "### Key Assumptions\n\n"
            "- limiar indicativo: 38/50;\n- volume ainda não medido;\n- custos relativos são hipóteses;\n"
            "- o corpus PDF foi inventariado, não integralmente validado obra a obra."
        ),
        code(
            "from pathlib import Path\nimport pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n"
            "root = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\n"
            "scores = pd.read_csv(root / 'data' / 'candidate_scores.csv')\n"
            "criteria = ['specialization','error_risk','method_independence','own_tools','work_volume','reuse','parallelism','own_memory','independent_audit','final_impact']\n"
            "scores['recomputed_total'] = scores[criteria].sum(axis=1)\n"
            "assert (scores['recomputed_total'] == scores['total']).all()\n"
            "scores[['candidate_id','candidate_name','total','final_id','disposition']].head()"
        ),
        md("## Data"),
        code(
            "summary = {\n"
            "    'candidate_roles': len(scores),\n"
            "    'above_threshold': int((scores.total >= 38).sum()),\n"
            "    'distinct_final_ids_raw': scores.final_id.nunique(),\n"
            "    'recommended_agents': 27,\n"
            "}\nsummary"
        ),
        md("## Results"),
        code(
            "def tags(value):\n    return set(str(value).split(';')) if pd.notna(value) else set()\n"
            "def jaccard(a, b):\n    u = a | b\n    return len(a & b) / len(u) if u else 0.0\n"
            "rows = []\n"
            "for i, left in scores.iterrows():\n"
            "    for _, right in scores.iloc[i+1:].iterrows():\n"
            "        overlap = 100 * (\n"
            "            .50*jaccard(tags(left.function_tags), tags(right.function_tags)) +\n"
            "            .15*jaccard(tags(left.source_tags), tags(right.source_tags)) +\n"
            "            .15*jaccard(tags(left.tool_tags), tags(right.tool_tags)) +\n"
            "            .20*jaccard(tags(left.output_tags), tags(right.output_tags))\n"
            "        )\n"
            "        reviewer_ids = {'C06','C33','C34','C35'}\n"
            "        conflict = (left.candidate_id in reviewer_ids) != (right.candidate_id in reviewer_ids)\n"
            "        rows.append({'left': left.candidate_id, 'right': right.candidate_id, 'overlap': round(overlap,1),\n"
            "                     'independence_block': conflict})\n"
            "overlaps = pd.DataFrame(rows).sort_values('overlap', ascending=False)\n"
            "overlaps.head(15)"
        ),
        code(
            "scenario = pd.DataFrame(" + repr(SCENARIOS) + ")\n"
            "ax = scenario.set_index('scenario')[['agents','motors','gates']].plot(kind='bar', figsize=(10,5), color=['#345995','#D6A84B','#7A6F9B'])\n"
            "ax.set_title('Escalas arquiteturais')\nax.set_ylabel('Quantidade')\nax.set_xlabel('')\nax.grid(axis='y', alpha=.2)\nplt.tight_layout()\nplt.show()"
        ),
        code(
            "active_counts = pd.DataFrame([{'product': k, 'active_agents': len(v)} for k,v in " + repr(PRODUCT_MATRIX) + ".items()])\n"
            "active_counts.sort_values('active_agents', ascending=False)"
        ),
        md(
            "## Takeaways\n\n"
            "- O número recomendado é **27 agentes lógicos**, não 27 agentes acionados por caso.\n"
            "- O conjunto ativo normal fica entre 8 e 14 agentes, conforme o produto.\n"
            "- Os 35 candidatos acima do limiar foram reduzidos por oito fusões com modos internos, "
            "mantendo revisão independente.\n"
            "- A arquitetura deve permanecer `DRAFT` até pilotos sintéticos A-H e medição de retrabalho."
        ),
        ],
    }
    write_json(ROOT / "notebooks" / "architecture_scoring.ipynb", nb)


def main() -> None:
    write_json(ROOT / "config" / "agent_registry.json", {"schema_version": "1.0.0", "status": "DRAFT", "agents": AGENTS})
    write_json(ROOT / "config" / "motors.json", {"schema_version": "1.0.0", "motors": MOTORS})
    write_json(ROOT / "config" / "bases.json", {"schema_version": "1.0.0", "bases": BASES})
    write_json(ROOT / "config" / "skills.json", {"schema_version": "1.0.0", "skills": [{"id": f"S{i:02d}", "name": name} for i, name in enumerate(SKILLS, 1)]})
    write_json(ROOT / "config" / "gates.json", {"schema_version": "1.0.0", "gates": GATES})
    write_json(ROOT / "config" / "product_matrix.json", PRODUCT_MATRIX)
    write_json(ROOT / "data" / "scenarios.json", SCENARIOS)
    write_json(ROOT / "data" / "fusions.json", FUSIONS)
    build_notebook()


if __name__ == "__main__":
    main()
