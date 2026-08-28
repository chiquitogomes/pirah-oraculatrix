# Contratos de dados e passagem

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
