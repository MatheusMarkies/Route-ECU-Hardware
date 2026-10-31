# Bibliotecas do projeto ECTU

Projeto: `D:\Route-ECU-Hardware\ECTU.PrjPcb`.

Foram inventariadas 350 instancias em 12 folhas, com 61 simbolos distintos.

Copiados: 48 arquivos IntLib em `IntLib/`, 2 IntLib em `Referencias_divergentes/` e 4 arquivos SchLib/PcbLib em `Fontes/`.

Todos os arquivos copiados tiveram seus hashes SHA-256 comparados com a origem. Os documentos de projeto, esquematicos e PCB permaneceram identicos durante a coleta. A verificacao usa os arquivos salvos no disco; alteracoes ainda nao salvas no Altium nao estao incluidas.

## Cobertura

- 290 instancias: biblioteca com nome original, simbolo e nome de footprint encontrados.
- 13 instancias: simbolo e nome de footprint encontrados em biblioteca com nome diferente; o vinculo precisa ser revisado.
- 3 instancias: arquivos fonte SchLib/PcbLib preservados, sem IntLib correspondente.
- 44 instancias: bibliotecas nao localizadas (10 simbolos).

## Bibliotecas nao localizadas

| Simbolo | Biblioteca gravada | Instancias | Designadores |
|---|---|---:|---|
| 47352-1001 | 47352-1001.IntLib | 1 | J4 |
| 5007620483 | 5007620483.IntLib | 1 | J11 |
| 796739-2 | 796739-2.IntLib | 1 | J10 |
| 7447709330 | Altium_WE-PD_rev22g.IntLib | 2 | L1, L2 |
| RC1206FR-074K7L | RC1206FR-074K7L.IntLib | 34 | R34, R30, R32, R35, R31, R36, R33, R29, R28, R37, R21, R20, R19, R18, R27, R26, R14, R15, R13, R25, R24, R?, R?, R?, R78, R77, R103, R102, R101, R100, R111, R109, R108, R110 |
| STM32H743VIT6 | STM32H743VIT6.IntLib | 1 | U1 |
| TSM-103-01-L-SH | TSM-103-01-L-SH (1).IntLib | 1 | J1 |
| TSM-104-01-L-MT | TSM-104-01-L-MT.IntLib | 1 | J2 |
| TSM4NB65CH_C5G | TSM4NB65CH_C5G.IntLib | 1 | Q9 |
| USB-B1HSB6 | USB-B1HSB6.IntLib | 1 | X1 |

## Correspondencias que exigem revisao

- **ADG729BRUZ / ***: Nao ha IntLib correspondente. Foram preservados os arquivos fonte com o simbolo e o footprint solicitado. O esquematico e a SchLib conservam o caminho absoluto original para SamacSys.PcbLib; revisar o vinculo para a copia local antes de usar em outro PC.
- **MPXA4250AC6U / ***: Nao ha IntLib correspondente. Foram preservados os arquivos fonte com o simbolo e o footprint solicitado. O esquematico e a SchLib conservam o caminho absoluto original para SamacSys.PcbLib; revisar o vinculo para a copia local antes de usar em outro PC.
- **BLM18DN601SZ1D / BLM18DN601SZ1D.IntLib**: Simbolo e nome de footprint encontrados, mas o nome do arquivo difere da referencia gravada; revisar o vinculo no Altium.
- **MB85RC1MTPNF-G-JNERE1 / MB85RC1MTPNF-G-JNERE1.IntLib**: Nao ha IntLib correspondente. Foram preservados os arquivos fonte com o simbolo e o footprint solicitado.
- **SMF5.0A / SMF5.0A.IntLib**: Simbolo e nome de footprint encontrados, mas o nome do arquivo difere da referencia gravada; revisar o vinculo no Altium.
- **SP721ABTG / SP721ABTG.IntLib**: Simbolo e nome de footprint encontrados, mas o nome do arquivo difere da referencia gravada; revisar o vinculo no Altium.
- **SS34 / SS34 (1).IntLib**: Uma versao de mesmo nome foi preservada em Referencias_divergentes porque contem outro footprint: DIOM6859X262N
- **SS34 / SS34.IntLib**: Simbolo e nome de footprint encontrados, mas o nome do arquivo difere da referencia gravada; revisar o vinculo no Altium. Uma versao de mesmo nome foi preservada em Referencias_divergentes porque contem outro footprint: DIOM7959X265N
- **TIP142 / TIP142.IntLib**: Ha outra versao de mesmo nome com hash diferente; foi priorizada a biblioteca instalada. As demais origens constam em alternatives.

## Uso no Altium

A coleta copia e relaciona as bibliotecas; ela nao altera os vinculos dos componentes nem registra arquivos no PrjPcb. No painel Projects, use Add Existing to Project para adicionar as bibliotecas de IntLib e os arquivos de Fontes. Revise as correspondencias com outro nome e os caminhos absolutos SamacSys. Nao adicione automaticamente Referencias_divergentes: ela guarda duas variantes SS34 com footprints diferentes dos solicitados.

O arquivo ECTU_PCB.PcbDoc salvo tem zero componentes no stream Components6. Portanto, gerar uma biblioteca a partir dessa PCB nao recuperaria os footprints das bibliotecas faltantes.

Este conjunto ainda nao representa um projeto totalmente portatil: faltam as bibliotecas listadas e a revisao de vinculos. Nao foi realizado teste de abertura/atualizacao em outro PC.

## Rastreabilidade

- [Mapa por componente e caminhos originais](mapa_componentes.md)
- [Manifesto completo, alternativas e hashes](manifesto_bibliotecas.json)

Busca: arquivos IntLib nas unidades C: e D: acessiveis, bibliotecas instaladas no registro do Altium, arquivos fonte no D:, Documents do usuario e Documents/Altium publico. Tambem foram examinadas as listas de arquivos de 305 ZIPs em Downloads e no projeto; nao foram encontradas bibliotecas com os nomes pendentes dentro desses ZIPs. A unidade G: dos caminhos antigos nao esta montada.
