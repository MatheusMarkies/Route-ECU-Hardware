# Sensores de posição do pedal e da borboleta eletrônica

No acelerador eletrônico (*drive-by-wire*), o pedal envia à ECU dois sinais de posição, **APP1** e **APP2** (*Accelerator Pedal Position*). A ECU usa a posição validada do pedal para calcular o pedido de torque e definir a abertura desejada da borboleta. O motor do corpo de borboleta move a válvula, e **TPS1** e **TPS2** (*Throttle Position Sensor*) informam a abertura efetiva. A ECU usa esse retorno para corrigir a posição pelo controle em malha fechada. [Arquitetura de controle eletrônico da borboleta, SAE](https://saemobilus.sae.org/papers/architecture-electronic-throttle-control-systems-2003-01-0098)

## Pedal do acelerador 1 e 2 (APP1 e APP2)

Os dois canais medem o mesmo curso do pedal. No exemplo da imagem, cada canal tem uma escala própria, de modo que uma mesma posição do pedal produz tensões diferentes. A ECU converte cada tensão em posição pela curva de calibração do respectivo canal. É a posição calculada que deve concordar dentro da tolerância de diagnóstico. [Verificações dos sensores APP, Ford](https://www.fordservicecontent.com/Ford_Content/catalog/motorcraft/OBD_System_Operation_Update.pdf#page=106)

Como exemplo didático, considere APP1 de 0,5 a 4,5 V e APP2 de 0,25 a 2,25 V, ambos crescentes e lineares. A 50% do curso, APP1 mede 2,50 V e APP2 mede 1,25 V. As duas leituras indicam os mesmos 50%. As faixas reais dependem do pedal utilizado.

Para um canal linear, a conversão é `posição [%] = 100 × (Vmedida − Vrepouso) / (Vfim_de_curso − Vrepouso)`. Se o sensor tiver uma curva não linear, a conversão usa a curva calibrada. O diagnóstico verifica a faixa elétrica de cada sinal e a diferença entre as posições calculadas. Assim, uma tensão pode estar dentro da faixa e ainda indicar uma posição incompatível com o outro canal.

A imagem descreve uma reação que limita a solicitação do pedal ao valor mais baixo. Essa decisão se refere à posição ou ao torque calculado, pois as tensões usam escalas distintas. A reação à falha depende da calibração e da capacidade de identificar qual sinal falhou. Um exemplo documentado usa o canal identificado como válido com abertura limitada. [Estratégia de falha do ETCS-i, NASA/NHTSA](https://www.nhtsa.gov/sites/nhtsa.gov/files/nasa-ua_report.pdf)

## Corpo de borboleta 1 e 2 (TPS1 e TPS2)

Os dois canais medem a posição do mesmo eixo da borboleta. No exemplo da imagem, as tensões variam em sentidos opostos durante a abertura. A tabela atribui o sinal decrescente ao TPS1 e o crescente ao TPS2 para ilustrar a lógica. A associação entre canal, sentido e faixa deve seguir o corpo de borboleta utilizado. [Exemplo de canais com inclinações opostas, Ford](https://www.fordservicecontent.com/Ford_Content/catalog/motorcraft/OBDSM1802-2018.pdf#page=220)

| Abertura no exemplo linear | TPS1, decrescente | TPS2, crescente |
|---|---:|---:|
| 0% (fechada) | 4,5 V | 0,5 V |
| 25% | 3,5 V | 1,5 V |
| 50% | 2,5 V | 2,5 V |
| 100% (aberta) | 0,5 V | 4,5 V |

Nesse exemplo, `TPS1 + TPS2 ≈ 5,0 V` ao longo do curso. A ECU pode verificar a coerência convertendo cada canal em ângulo ou percentual de abertura e comparando os resultados. Por exemplo, 3,5 V nos dois canais corresponderiam a 25% no TPS1 e 75% no TPS2. As duas tensões estão dentro da faixa, mas a diferença de posição indica uma falha de plausibilidade. Uma segunda verificação compara a posição medida com a desejada e ajuda a detectar casos em que os dois canais concordam, mas a válvula fica presa ou deixa de acompanhar o comando. [Diagnóstico de posição e atuação da borboleta, Ford](https://www.fordservicecontent.com/ford_content/catalog/motorcraft/OBDSM1201_16.pdf)

## Sensor virtual com o MAF

O MAF (*Mass Air Flow*) mede a vazão mássica de ar admitido. Na estratégia descrita na imagem, se um TPS indica borboleta fechada e o outro indica abertura parcial, a ECU pode confrontar as duas leituras com uma estimativa baseada no escoamento. O sensor virtual é essa estimativa calculada em software. Um modelo calibrado pode verificar qual abertura é mais compatível com a vazão e com as condições de operação, como rotação e pressões de admissão. A estimativa tem incerteza, especialmente durante transientes. Sua utilização no diagnóstico depende da validade do MAF e do modelo naquele ponto de operação. [Diagnóstico de admissão baseado em modelo, SAE](https://saemobilus.sae.org/papers/model-based-diagnosis-air-intake-system-si-engine-970209)

## Aplicação na Route ECU (ECTU)

O mapeamento abaixo foi conferido na conectividade compilada do esquemático em 07/11/2026. Os pinos de J11 são da ECU. [Folha de aquisição](ExternalInterface.SchDoc) · [Alocação dos conectores](docs/ALOCACAO_CONECTORES.md) · [Pinagem do ADS8688, Texas Instruments](https://www.ti.com/lit/ds/symlink/ads8688.pdf)

| Sinal | Conector | Rede | Entrada do ADC (ADS8688) |
|---|---|---|---|
| Pedal 1 (APP1) | J11-B3 | `APP1_ADC` | U6 `AIN_7P`, pino 14 |
| Pedal 2 (APP2) | J11-B4 | `APP2_ADC` | U7 `AIN_5P`, pino 27 |
| Borboleta 1 (TPS1) | J11-B1 | `TPS1_ADC` | U6 `AIN_5P`, pino 27 |
| Borboleta 2 (TPS2) | J11-B2 | `TPS2_ADC` | U6 `AIN_6P`, pino 12 |
| MAF externo | J11-A2 | `MAF_EXT_IN` → `MAF_EXT_ADC` | U6 `AIN_2P`, pino 21 |

A ponte H U33 (`DRV8873HPWPRQ1`) aciona o motor pelos pinos J12-28 e J12-29 (`ETC_OUT1` e `ETC_OUT2`). Os dois TPS chegam ao U6, enquanto APP1 e APP2 usam ADCs distintos. O APP2 ocupa o antigo canal AUX6 e segue a mesma topologia do APP1, com R37 (4,7 kΩ) e C48 (100 nF) ligados ao GND e proteção pelo SP721 U12 no pino 3. O J11-E2 ficou reservado. As faixas dos sensores, os limites de plausibilidade e as reações de falha apresentados acima são referências de funcionamento. O diagnóstico cruzado, a calibração, o sensor virtual e a atuação sob falha requerem validação em firmware e bancada. [Descrição do hardware da ECTU](README.md)

## Topologia proposta para os sensores de pressão de freio

Usar um transdutor na saída do cilindro-mestre dianteiro e outro na saída do traseiro. Cada transdutor mede a pressão do próprio circuito hidráulico. A regra T.3.1.3 exige dois circuitos hidráulicos independentes. Usar um transdutor em cada circuito é a opção da ECTU para medir as duas pressões. [Regulamento Formula SAE 2026, T.3.1 e T.4.3](https://www.fsaeonline.com/cdsweb/gen/DownloadDocument.aspx?DocumentID=278fd4d7-aa27-4e33-bc4a-090148e662a0#page=64)

| Circuito | Entrada a reaproveitar | Rede proposta | Canal do ADC | Componentes da entrada atual |
|---|---|---|---|---|
| Dianteiro | `J11-D4` (`AUX4_ADC`) | `BSE_F_ADC` | U7 `AIN_3P`, pino 23 | R38, C49 e proteção U12, pino 6 |
| Traseiro | `J11-E1` (`AUX5_ADC`) | `BSE_R_ADC` | U7 `AIN_4P`, pino 25 | R39, C50 e proteção U12, pino 5 |

O circuito proposto reaproveita a topologia das entradas de pressão de óleo e combustível. Cada sinal tem pull-up de 4,7 kΩ para `V5V0_SENS`, capacitor de 100 nF para GND e proteção pelo SP721. O pull-up leva a entrada para perto de 5 V quando o fio de sinal é aberto. A detecção desse estado depende da faixa de saída do sensor escolhido e da calibração. A premissa é usar transdutores analógicos de três fios, com `V5V0_SENS`, retorno de sensores e sinal de aproximadamente 0,5 a 4,5 V na faixa nominal. Com essa alocação, `AUX1_ADC` a `AUX3_ADC` ficam disponíveis para outras funções. [Folha de aquisição](ExternalInterface.SchDoc) · [Alocação atual do J11](docs/ALOCACAO_CONECTORES.md) · [T.4.3.4](https://www.fsaeonline.com/cdsweb/gen/DownloadDocument.aspx?DocumentID=278fd4d7-aa27-4e33-bc4a-090148e662a0#page=67)

Cada sinal de pressão fica disponível no conector para dois caminhos em paralelo. Um vai ao U7 para leitura pelo H7. O outro leva o sinal bruto à entrada do futuro BSPD, antes da conversão pelo ADC. A forma de combinar as duas pressões para identificar frenagem forte fica em aberto, assim como os limiares de falha, a compatibilidade do transdutor com a carga do pull-up e do BSPD, a faixa de pressão e a especificação da rosca, vedação e fluido. [IC.4.8.3–4](https://www.fsaeonline.com/cdsweb/gen/DownloadDocument.aspx?DocumentID=278fd4d7-aa27-4e33-bc4a-090148e662a0#page=84)

## Pontos em aberto para revisão do ETC na Fórmula SAE Brasil

Os limites abaixo usam como referência o regulamento de 2026. A conferência da conectividade do esquemático já foi feita. Os itens a seguir dependem da revisão do veículo, do firmware ou de ensaios. [Adendo brasileiro v1.3](https://arquivos.saebrasil.org.br/2026/Formula/FSAEB_2026_Rules_Addendum_V1.3.pdf)

### Hardware e chicote

- [ ] **Adicionar o BSPD à ECU.** Incluir no hardware da ECTU um circuito autônomo, sem componentes programáveis, com alimentação que possa ser interrompida separadamente no teste e entradas diretas para os sinais brutos de freio e TPS. Traçar como ele abre o *Shutdown Circuit* e corta a alimentação da ponte H U33, da bomba e da ignição. Conferir o caminho de potência de `VBAT_ECU` até U33 e separar esse corte do comando `ETC_SLEEP_N` do H7. [IC.4.8 e IC.9.2](https://www.fsaeonline.com/cdsweb/gen/DownloadDocument.aspx?DocumentID=278fd4d7-aa27-4e33-bc4a-090148e662a0#page=84)
- [ ] **Pedal e APP1/APP2.** Confirmar que o pedal tem dois sensores eletricamente separados. Medir as duas curvas no curso todo e verificar a separação mínima de 10% entre as saídas quando o pedal estiver acima de 10% do curso, conforme T.4.2.3. Desconectar cada sinal para confirmar que o pull-down leva a entrada à condição de 0% e que a ECU acusa falha. Ensaiar também curto a GND, à alimentação e entre sinais. [T.4.2](https://www.fsaeonline.com/cdsweb/gen/DownloadDocument.aspx?DocumentID=278fd4d7-aa27-4e33-bc4a-090148e662a0#page=65)
- [ ] **Borboleta e TPS1/TPS2.** Levantar as curvas reais dos dois TPS. Testar se os pull-ups permitem detectar circuito aberto e se os curtos geram falha. Como ambos entram no U6, verificar o comportamento perante falha do ADC. Se o chicote compartilhar alimentação ou referência entre os TPS, demonstrar a detecção de desvios nessas linhas. [IC.4.4](https://www.fsaeonline.com/cdsweb/gen/DownloadDocument.aspx?DocumentID=278fd4d7-aa27-4e33-bc4a-090148e662a0#page=83)
- [ ] **Adicionar as entradas BSE dianteira e traseira à ECU.** Confirmar os dois transdutores e revisar a alocação e o condicionamento descritos na topologia proposta. Levar os dois sinais brutos diretamente ao BSPD. Calibrar a condição de frenagem forte e verificar como cada circuito detecta perda de sinal. [T.4.3](https://www.fsaeonline.com/cdsweb/gen/DownloadDocument.aspx?DocumentID=278fd4d7-aa27-4e33-bc4a-090148e662a0#page=67) · [IC.4.8](https://www.fsaeonline.com/cdsweb/gen/DownloadDocument.aspx?DocumentID=278fd4d7-aa27-4e33-bc4a-090148e662a0#page=84)
- [ ] **Retorno mecânico.** Testar o retorno do pedal a 0% com cada mola atuando sozinha. Verificar o batente e medir a posição de repouso da borboleta sem alimentação no motor. Confirmar o retorno à marcha lenta. [T.4.2](https://www.fsaeonline.com/cdsweb/gen/DownloadDocument.aspx?DocumentID=278fd4d7-aa27-4e33-bc4a-090148e662a0#page=65) · [IC.4.1](https://www.fsaeonline.com/cdsweb/gen/DownloadDocument.aspx?DocumentID=278fd4d7-aa27-4e33-bc4a-090148e662a0#page=82)

### Firmware e ensaios

- [ ] **Corte por falha de sensor.** Verificar o corte de potência do atuador quando APP1/APP2 ou TPS1/TPS2 divergirem em mais de 10 pontos percentuais por mais de 100 ms. Injetar falhas de sensor e chicote, incluindo perda do BSE por mais de 100 ms. Com dois canais, a reação à divergência persistente é o corte. [T.4.2–T.4.3](https://www.fsaeonline.com/cdsweb/gen/DownloadDocument.aspx?DocumentID=278fd4d7-aa27-4e33-bc4a-090148e662a0#page=66) · [IC.4.4](https://www.fsaeonline.com/cdsweb/gen/DownloadDocument.aspx?DocumentID=278fd4d7-aa27-4e33-bc4a-090148e662a0#page=83)
- [ ] **Freio × abertura e abertura × alvo.** Definir a abertura permitida com o freio acionado. Ensaiar o corte do atuador após mais de 1 s de abertura acima desse limite com freio acionado, ou de erro acima de 10 pontos percentuais entre a abertura medida e a comandada. Ensaiar o corte de combustível e ignição se a posição não se recuperar no segundo seguinte. Verificar a retenção do desligamento até os TPS indicarem posição igual ou inferior à posição desenergizada por pelo menos 1 s. [IC.4.7](https://www.fsaeonline.com/cdsweb/gen/DownloadDocument.aspx?DocumentID=278fd4d7-aa27-4e33-bc4a-090148e662a0#page=84)
- [ ] **Disparo e reset do BSPD.** Ensaiar frenagem forte com abertura acima de 10% por mais de 1 s, perda de sinal de freio ou TPS por mais de 100 ms e perda de alimentação do próprio BSPD. Conferir a abertura do *Shutdown Circuit* e o reset pelo ciclo da chave geral principal após disparo. No teste de perda de alimentação do BSPD, o circuito pode fechar quando a alimentação voltar. [IC.4.8](https://www.fsaeonline.com/cdsweb/gen/DownloadDocument.aspx?DocumentID=278fd4d7-aa27-4e33-bc4a-090148e662a0#page=84)

### PCB, documentação e inspeção

- [ ] **ECO e exportações.** Aplicar o ECO na PCB, conferir `J11-B4 → APP2_ADC → U7-27`, `R37 → GND` e `J11-E2` livre. Rodar DRC e atualizar a netlist e o PDF da revisão.
- [ ] **Acesso para inspeção.** Prever conectores ou uma *breakout box* para interromper individualmente os sinais de APP, TPS e BSE. Prever também um meio de desligar somente a alimentação do BSPD. Registrar os tempos medidos, a abertura da borboleta e os cortes de potência, combustível e ignição nos ensaios. [T.4.2.7, T.4.3.2 e IC.4.8.9](https://www.fsaeonline.com/cdsweb/gen/DownloadDocument.aspx?DocumentID=278fd4d7-aa27-4e33-bc4a-090148e662a0)
- [ ] **Regulamento da edição e submissões.** Confirmar a versão do regulamento-base e o adendo brasileiro da edição em que o carro vai competir. Preparar o *ETC Notice of Intent* (`ETCNI`) e o *ETC Systems Form* (`ETCSF`) com os circuitos, a lógica de falha e as evidências de ensaio. Conferir os prazos e os modelos publicados pela organização. [Publicações da Fórmula SAE Brasil](https://saebrasil.org.br/formula-sae-brasil-mensagens-e-informativos/)

## Pendência de instrumentação do motor

Proposta para registrar a pressão de um cilindro em função do ângulo do virabrequim. A instrumentação fica em uma seção própria de desenvolvimento do motor, separada da revisão do ETC e do BSPD.

- [ ] **Definir sensor, condicionamento e chicote.** Selecionar o transdutor e dimensionar o circuito de entrada para a faixa e a banda do ADC interno do G071. Para sensor piezoelétrico com saída em carga, prever amplificador de carga. O pino candidato para a pressão condicionada é `PB2 / ADC_IN10` (pino 29) do G071. Definir a posição no conector e revisar proteção, filtro e atraso do sinal. [Datasheet do STM32G071](https://www.st.com/resource/en/datasheet/stm32g071rb.pdf)
- [ ] **Levar a referência angular ao G071.** Derivar `CKP_MCU` da saída `IC4-4` do seletor VR/Hall para `PB0 / TIM3_CH3` (pino 27). Para distinguir as duas voltas do ciclo de 720°, derivar também `CMP_MCU` de `IC3-4` para `PB1 / TIM3_CH4` (pino 28). Conferir as bordas após a derivação nos dois MCUs. [Esquemático CKP/CMP](CrankAndCam.SchDoc) · [ECO dos seletores](Project%20Logs%20for%20ECTU/ECTU_PCB%20PCB%20ECO%2004-11-2026%2010-40-32.LOG)
- [ ] **Capturar pressão e dentes na mesma base de tempo.** Usar o `TIM3` para carimbar as bordas e iniciar o `TIM1` via `ITR2`. Disparar o ADC com `TIM1_TRGO2` e coletar por DMA em blocos. A meta inicial para um sensor é **400 kS/s**, com **2,5 µs** entre amostras e **0,24°** de espaçamento nominal a **16.000 rpm**. Registrar o instante inicial, o período e o índice de cada bloco, além das marcas CKP/CMP na mesma base de tempo. Tratar a volta do contador do `TIM3` e sinalizar perdas de dados. [Disparos do ADC](https://www.st.com/resource/en/reference_manual/rm0444-stm32g0x1-advanced-armbased-32-bit-mcus-stmicroelectronics.pdf#page=344) · [Ligação interna entre timers](https://www.st.com/resource/en/reference_manual/rm0444-stm32g0x1-advanced-armbased-32-bit-mcus-stmicroelectronics.pdf#page=582)
- [ ] **Gravar no microSD e validar o ângulo.** Enviar os blocos do G071 ao H743 pelo SPI dedicado e gravar no microSD do H7 para análise posterior no Workbench. A meta de 400 kS/s representa **0,8 MB/s** em palavras de 16 bits, além das marcas e dos cabeçalhos. Reconstruir o ângulo entre as bordas do CKP, considerar o vão da roda fônica e calibrar a referência do PMS e o atraso do condicionamento. Na roda de teste 60-2, usar **6°** entre dentes consecutivos e **18°** no vão. Medir perdas, erro angular e interferência na temporização de ignição e injeção durante a gravação. [Enlace H7–G0](README.md#spi-dedicado-entre-h7-e-g0) · [Armazenamento da ECTU](README.md#hardware-desta-versão)
